import ast
import pprint
import textwrap
from pathlib import Path

from django.utils import timezone as django_timezone

from llm.models import AgentTool

from . import GENERATED_DIR

FILE_TEMPLATE = '''\
"""Auto-generated tool: {name}. Regenerate from Django admin."""

from __future__ import annotations

SCHEMA = {schema}


def {name}(**kwargs):
{body}
'''


def _default_parameters() -> dict:
    return {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }


def validate_python_body(python_code: str) -> None:
    wrapped = f"def _validate(**kwargs):\n{textwrap.indent(python_code, '    ')}"
    ast.parse(wrapped)


def build_schema(tool: AgentTool) -> dict:
    parameters = tool.parameters or _default_parameters()
    return {
        "name": tool.name,
        "description": tool.description,
        "parameters": parameters,
    }


def build_file_content(tool: AgentTool) -> str:
    schema = build_schema(tool)
    schema_repr = pprint.pformat(schema, indent=4, sort_dicts=False)
    body = textwrap.indent(tool.python_code.rstrip(), "    ")
    return FILE_TEMPLATE.format(
        name=tool.name,
        schema=schema_repr,
        body=body,
    )


def generated_file_path(tool: AgentTool) -> Path:
    return GENERATED_DIR / f"{tool.name}.py"


def write_tool_file(tool: AgentTool) -> Path:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    validate_python_body(tool.python_code)

    path = generated_file_path(tool)
    path.write_text(build_file_content(tool), encoding="utf-8")
    return path


def generate_tool_file(tool: AgentTool) -> Path:
    path = write_tool_file(tool)
    tool.file_generated = True
    tool.generated_file = f"llm/tools/generated/{tool.name}.py"
    tool.generated_at = django_timezone.now()
    tool.save(
        update_fields=[
            "file_generated",
            "generated_file",
            "generated_at",
            "updated_at",
        ]
    )
    return path


def delete_tool_file(tool: AgentTool) -> None:
    path = generated_file_path(tool)
    if path.exists():
        path.unlink()
