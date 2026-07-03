from django.db import models


class LlmModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "LLM Model"
        verbose_name_plural = "LLM Models"

    def __str__(self) -> str:
        status = "active" if self.active else "inactive"
        return f"{self.name} ({status})"


class LlmAgent(models.Model):
    model = models.ForeignKey(
        LlmModel,
        on_delete=models.PROTECT,
        related_name="agents",
        limit_choices_to={"active": True},
    )
    name = models.CharField(max_length=255, unique=True)
    role = models.CharField(
        max_length=255,
        help_text="System role for the agent, e.g. 'You are a helpful assistant.'",
    )
    context = models.TextField(
        blank=True,
        help_text="Additional system context or instructions for the agent.",
    )
    use_other_agent = models.BooleanField(
        default=False,
        help_text="Use a custom OpenAI-compatible endpoint (Ollama, Gemini, etc.).",
    )
    base_url = models.URLField(
        blank=True,
        help_text="Required when using another agent, e.g. http://localhost:11434/v1",
    )
    api_key = models.CharField(
        max_length=512,
        help_text="API key for OpenAI or the compatible provider.",
    )
    tools = models.ManyToManyField(
        "AgentTool",
        blank=True,
        related_name="agents",
        help_text="Tools this agent may call via the LLM.",
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "LLM Agent"
        verbose_name_plural = "LLM Agents"

    def __str__(self) -> str:
        return f"{self.name} ({self.model.name})"


class AgentTool(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Snake_case function name, e.g. get_ticket_price",
    )
    description = models.TextField(
        help_text="Description shown to the LLM for when to use this tool.",
    )
    parameters = models.JSONField(
        default=dict,
        help_text="OpenAI function parameters JSON schema (type, properties, required).",
    )
    python_code = models.TextField(
        help_text=(
            "Python function body. Use kwargs, e.g. "
            'city = kwargs["destination_city"]'
        ),
    )
    active = models.BooleanField(default=True)
    file_generated = models.BooleanField(default=False, editable=False)
    generated_file = models.CharField(max_length=255, blank=True, editable=False)
    generated_at = models.DateTimeField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Agent Tool"
        verbose_name_plural = "Agent Tools"

    def __str__(self) -> str:
        status = "generated" if self.file_generated else "draft"
        return f"{self.name} ({status})"

    def delete(self, *args, **kwargs):
        from llm.tools.generator import delete_tool_file

        delete_tool_file(self)
        super().delete(*args, **kwargs)


class ChatMessage(models.Model):
    class Role(models.TextChoices):
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"

    event_id = models.CharField(max_length=64, db_index=True)
    agent = models.ForeignKey(
        LlmAgent,
        on_delete=models.CASCADE,
        related_name="chat_messages",
    )
    role = models.CharField(max_length=16, choices=Role.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["event_id", "agent"]),
        ]

    def __str__(self) -> str:
        return f"{self.event_id} / {self.agent.name} / {self.role}"
