import json

from django import forms
from django.contrib import admin, messages
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

from llm.tools.generator import generate_tool_file, validate_python_body
from llm.tools.registry import reload_registry
from llm.widgets import JsonAceWidget, PythonAceWidget

from .models import AgentTask, AgentTool, ChatMessage, LlmAgent, LlmModel, Project
from .vector_store import (
    clear_agent_collection,
    collection_name_for_agent,
    reset_agent_task_vector_flags,
)
from .vector_visualization import build_plotly_html


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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "active", "updated_at")
    list_filter = ("active",)
    search_fields = ("name", "description")
    list_editable = ("active",)


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
        "vector_db_link",
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/vector-visualization/",
                self.admin_site.admin_view(self.vector_visualization_view),
                name="llm_llmagent_vector_visualization",
            ),
            path(
                "<path:object_id>/clear-vector-db/",
                self.admin_site.admin_view(self.clear_vector_db_view),
                name="llm_llmagent_clear_vector_db",
            ),
        ]
        return custom_urls + urls

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        if obj:
            fieldsets.append(
                (
                    "Vector database",
                    {
                        "fields": ("vector_db_link",),
                        "description": (
                            "Visualize or clear this agent's PGVector collection. "
                            "Clearing resets task vector flags."
                        ),
                    },
                )
            )
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("vector_db_link",)
        return ()

    @admin.display(description="Vector DB")
    def vector_db_link(self, obj):
        if not obj.pk:
            return "—"
        visualize_url = reverse("admin:llm_llmagent_vector_visualization", args=[obj.pk])
        clear_url = reverse("admin:llm_llmagent_clear_vector_db", args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">Visualize vector DB</a>&nbsp;'
            '<a class="button" href="{}">Clear vector DB</a>',
            visualize_url,
            clear_url,
        )

    def clear_vector_db_view(self, request, object_id):
        agent = get_object_or_404(LlmAgent, pk=object_id)
        point_count = 0
        try:
            from .vector_visualization import fetch_collection_rows

            point_count = len(fetch_collection_rows(agent.pk))
        except Exception:
            point_count = 0

        if request.method == "POST":
            try:
                deleted = clear_agent_collection(agent.pk)
                reset_count = reset_agent_task_vector_flags(agent.pk)
                self.message_user(
                    request,
                    f"Cleared {deleted} vector(s) and reset {reset_count} task(s) for {agent.name}.",
                    level=messages.SUCCESS,
                )
            except Exception as exc:
                self.message_user(
                    request,
                    f"Failed to clear vector DB: {exc}",
                    level=messages.ERROR,
                )
            return TemplateResponse(
                request,
                "admin/llm/llmagent/clear_vector_db.html",
                {
                    **self.admin_site.each_context(request),
                    "title": f"Clear vector DB — {agent.name}",
                    "agent": agent,
                    "collection_name": collection_name_for_agent(agent.pk),
                    "point_count": 0,
                    "cleared": True,
                    "opts": self.model._meta,
                },
            )

        context = {
            **self.admin_site.each_context(request),
            "title": f"Clear vector DB — {agent.name}",
            "agent": agent,
            "collection_name": collection_name_for_agent(agent.pk),
            "point_count": point_count,
            "cleared": False,
            "opts": self.model._meta,
        }
        return TemplateResponse(
            request,
            "admin/llm/llmagent/clear_vector_db.html",
            context,
        )

    def vector_visualization_view(self, request, object_id):
        agent = get_object_or_404(LlmAgent, pk=object_id)

        try:
            dims = int(request.GET.get("dims", "2"))
        except (TypeError, ValueError):
            dims = 2
        if dims not in (2, 3):
            dims = 2

        plot_html = ""
        point_count = 0
        error = None
        try:
            plot_html, point_count = build_plotly_html(agent.pk, dims)
        except Exception as exc:
            error = str(exc)

        context = {
            **self.admin_site.each_context(request),
            "title": f"Vector DB — {agent.name}",
            "agent": agent,
            "dims": dims,
            "collection_name": collection_name_for_agent(agent.pk),
            "plot_html": plot_html,
            "point_count": point_count,
            "error": error,
            "opts": self.model._meta,
        }
        return TemplateResponse(
            request,
            "admin/llm/llmagent/vector_visualization.html",
            context,
        )


@admin.register(AgentTask)
class AgentTaskAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "agent", "vd_processed", "processed", "created_at")
    list_filter = ("vd_processed", "processed", "agent", "project")
    search_fields = ("name", "vd_name", "description", "result", "project__name")
    readonly_fields = ("vd_name", "created_at", "updated_at")
    autocomplete_fields = ("agent", "project")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("event_id", "agent", "role", "created_at")
    list_filter = ("role", "agent")
    search_fields = ("event_id", "content")
    readonly_fields = ("event_id", "agent", "role", "content", "created_at")
