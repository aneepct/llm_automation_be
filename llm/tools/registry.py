import importlib.util
from typing import Any, Callable

from . import GENERATED_DIR

ToolHandler = Callable[..., Any]
_registry: dict[str, dict[str, Any]] | None = None


def _load_module(path):
    spec = importlib.util.spec_from_file_location(f"llm.tools.generated.{path.stem}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load tool module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_registry(force_reload: bool = False) -> dict[str, dict[str, Any]]:
    global _registry
    if _registry is not None and not force_reload:
        return _registry

    registry: dict[str, dict[str, Any]] = {}
    if not GENERATED_DIR.exists():
        _registry = registry
        return registry

    for path in sorted(GENERATED_DIR.glob("*.py")):
        if path.name.startswith("_"):
            continue
        try:
            module = _load_module(path)
        except Exception:
            continue

        schema = getattr(module, "SCHEMA", None)
        if not schema or "name" not in schema:
            continue

        name = schema["name"]
        handler = getattr(module, name, None)
        if not callable(handler):
            continue

        registry[name] = {
            "schema": schema,
            "handler": handler,
            "path": str(path),
        }

    _registry = registry
    return registry


def reload_registry() -> dict[str, dict[str, Any]]:
    return load_registry(force_reload=True)


def get_openai_tools(tool_names: list[str]) -> list[dict]:
    registry = load_registry()
    tools = []
    for name in tool_names:
        entry = registry.get(name)
        if not entry:
            continue
        tools.append({"type": "function", "function": entry["schema"]})
    return tools


def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    registry = load_registry()
    entry = registry.get(name)
    if not entry:
        return f"Error: unknown tool '{name}'"

    try:
        result = entry["handler"](**arguments)
        return str(result)
    except Exception as exc:
        return f"Error running tool '{name}': {exc}"


def test_tool(name: str, arguments: dict[str, Any]) -> str:
    reload_registry()
    return execute_tool(name, arguments)
