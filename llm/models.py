import re

from django.db import models


def slugify_task_name(name: str) -> str:
    slug = name.strip().lower().replace(" ", "_")
    slug = re.sub(r"[^a-z0-9_]", "", slug)
    return slug or "task"


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


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        status = "active" if self.active else "inactive"
        return f"{self.name} ({status})"


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


class AgentTask(models.Model):
    agent = models.ForeignKey(
        LlmAgent,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="tasks",
    )
    name = models.CharField(max_length=255)
    vd_name = models.CharField(max_length=255, editable=False)
    description = models.TextField()
    result = models.TextField(blank=True)
    vd_processed = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Agent Task"
        verbose_name_plural = "Agent Tasks"
        constraints = [
            models.UniqueConstraint(
                fields=["agent", "vd_name"],
                name="unique_agent_task_vd_name",
            )
        ]

    def __str__(self) -> str:
        return f"{self.agent.name} / {self.project.name} / {self.name}"

    def save(self, *args, **kwargs):
        if self.agent_id:
            self.vd_name = unique_vd_name_for_agent(
                self.agent_id,
                self.name,
                exclude_pk=self.pk,
            )
        else:
            self.vd_name = slugify_task_name(self.name)
        super().save(*args, **kwargs)


def unique_vd_name_for_agent(
    agent_id: int,
    name: str,
    *,
    exclude_pk: int | None = None,
) -> str:
    base_slug = slugify_task_name(name)
    slug = base_slug
    counter = 2
    while True:
        queryset = AgentTask.objects.filter(agent_id=agent_id, vd_name=slug)
        if exclude_pk is not None:
            queryset = queryset.exclude(pk=exclude_pk)
        if not queryset.exists():
            return slug
        slug = f"{base_slug}_{counter}"
        counter += 1


class WebsiteKnowledgeJob(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    agent = models.ForeignKey(
        LlmAgent,
        on_delete=models.CASCADE,
        related_name="website_knowledge_jobs",
    )
    root_url = models.URLField()
    selected_urls = models.JSONField(default=list)
    use_llm_cleanup = models.BooleanField(default=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )
    completed_count = models.PositiveIntegerField(default=0)
    total_count = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Website Knowledge Job"
        verbose_name_plural = "Website Knowledge Jobs"

    def __str__(self) -> str:
        return f"{self.agent.name} / {self.root_url} ({self.status})"

