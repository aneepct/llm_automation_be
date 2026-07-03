import json

from django import forms
from django.contrib import admin, messages
from django.utils.html import format_html

from llm.tools.generator import generate_tool_file, validate_python_body
from llm.tools.registry import reload_registry
from llm.widgets import JsonAceWidget, PythonAceWidget

from .models import AgentTool, ChatMessage, LlmAgent, LlmModel


class LlmAgentAdminForm(forms.ModelForm):
    class Meta:
        model = LlmAgent
        fields = "__all__"
        widgets = {
            "api_key": forms.PasswordInput(render_value=True),
        }

    def clean(self):
        cleaned_data = super().clean()
        use_other_agent = cleaned_data.get("use_other_agent")
        base_url = cleaned_data.get("base_url")

        if use_other_agent and not base_url:
            raise forms.ValidationError(
                {"base_url": "Base URL is required when using another agent."}
            )

        if not cleaned_data.get("api_key"):
            raise forms.ValidationError({"api_key": "API key is required."})

        return cleaned_data


class AgentToolAdminForm(forms.ModelForm):
    class Meta:
        model = AgentTool
        fields = "__all__"
        widgets = {
            "python_code": PythonAceWidget(),
            "parameters": JsonAceWidget(),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name.replace("_", "").isalnum() or name != name.lower():
            raise forms.ValidationError("Name must be snake_case (lowercase letters, numbers, underscores).")
        return name

    def clean_python_code(self):
        code = self.cleaned_data["python_code"]
        validate_python_body(code)
        return code

    def clean_parameters(self):
        value = self.cleaned_data.get("parameters")
        if value in (None, ""):
            return {}
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError as exc:
                raise forms.ValidationError(f"Invalid JSON: {exc}") from exc
        return value


@admin.register(LlmModel)
class LlmModelAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "active", "updated_at")
    list_filter = ("active",)
    search_fields = ("name", "description")
    list_editable = ("active",)


@admin.register(AgentTool)
class AgentToolAdmin(admin.ModelAdmin):
    form = AgentToolAdminForm
    list_display = (
        "name",
        "active",
        "file_generated",
        "generated_at",
        "updated_at",
    )
    list_filter = ("active", "file_generated")
    search_fields = ("name", "description")
    readonly_fields = ("file_generated", "generated_file", "generated_at")
    actions = ("generate_python_files", "reload_tool_registry")

    class Media:
        css = {"all": ("llm/admin/agent_tool.css",)}

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "parameters",
                    "active",
                )
            },
        ),
        (
            "Python implementation",
            {
                "fields": ("python_code",),
                "description": (
                    "Write the function body only. Arguments arrive in kwargs. "
                    'Example: city = kwargs["destination_city"]'
                ),
            },
        ),
        (
            "Generated file",
            {
                "fields": (
                    "file_generated",
                    "generated_file",
                    "generated_at",
                ),
            },
        ),
    )

    @admin.action(description="Generate Python tool files")
    def generate_python_files(self, request, queryset):
        success = 0
        for tool in queryset:
            try:
                path = generate_tool_file(tool)
                success += 1
                self.message_user(
                    request,
                    f"Generated {tool.name} → {path}",
                    level=messages.SUCCESS,
                )
            except Exception as exc:
                self.message_user(
                    request,
                    f"Failed to generate {tool.name}: {exc}",
                    level=messages.ERROR,
                )

        if success:
            reload_registry()

    @admin.action(description="Reload tool registry")
    def reload_tool_registry(self, request, queryset):
        registry = reload_registry()
        self.message_user(
            request,
            f"Loaded {len(registry)} tool(s) from llm/tools/generated/",
            level=messages.INFO,
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.python_code.strip():
            try:
                generate_tool_file(obj)
                reload_registry()
                self.message_user(
                    request,
                    format_html("Generated tool file for <strong>{}</strong>.", obj.name),
                    level=messages.SUCCESS,
                )
            except Exception as exc:
                self.message_user(
                    request,
                    f"Saved tool but file generation failed: {exc}",
                    level=messages.WARNING,
                )


@admin.register(LlmAgent)
class LlmAgentAdmin(admin.ModelAdmin):
    form = LlmAgentAdminForm
    list_display = (
        "name",
        "model",
        "use_other_agent",
        "active",
        "updated_at",
    )
    list_filter = ("active", "use_other_agent", "model")
    search_fields = ("name", "role", "context")
    list_editable = ("active",)
    autocomplete_fields = ("model",)
    filter_horizontal = ("tools",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "model",
                    "tools",
                    "active",
                )
            },
        ),
        (
            "Behavior",
            {
                "fields": (
                    "role",
                    "context",
                )
            },
        ),
        (
            "Provider",
            {
                "fields": (
                    "use_other_agent",
                    "base_url",
                    "api_key",
                ),
                "description": (
                    "Leave base URL empty for OpenAI. "
                    "When using another agent, set base URL and API key "
                    "(e.g. Ollama: http://localhost:11434/v1 with api_key 'ollama')."
                ),
            },
        ),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("event_id", "agent", "role", "created_at")
    list_filter = ("role", "agent")
    search_fields = ("event_id", "content")
    readonly_fields = ("event_id", "agent", "role", "content", "created_at")
