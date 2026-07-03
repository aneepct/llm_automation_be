import json

from django_ace import AceWidget

EDITOR_DEFAULTS = {
    "width": "100%",
    "toolbar": True,
    "showgutter": True,
    "showprintmargin": True,
    "tabsize": 4,
    "usesofttabs": True,
    "basicautocompletion": True,
    "liveautocompletion": True,
    "fontsize": "14px",
}


class PythonAceWidget(AceWidget):
    def __init__(self, **kwargs):
        options = {
            **EDITOR_DEFAULTS,
            "mode": "python",
            "theme": "monokai",
            "height": "420px",
            "minlines": 16,
            "maxlines": 40,
        }
        options.update(kwargs)
        super().__init__(**options)


class JsonAceWidget(AceWidget):
    def __init__(self, **kwargs):
        options = {
            **EDITOR_DEFAULTS,
            "mode": "json",
            "theme": "monokai",
            "height": "280px",
            "minlines": 10,
            "maxlines": 30,
        }
        options.update(kwargs)
        super().__init__(**options)

    def format_value(self, value):
        if value in (None, ""):
            return ""
        if isinstance(value, (dict, list)):
            return json.dumps(value, indent=2, sort_keys=False)
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                return json.dumps(parsed, indent=2, sort_keys=False)
            except json.JSONDecodeError:
                return value
        return str(value)
