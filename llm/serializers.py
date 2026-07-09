from rest_framework import serializers

from .models import AgentTask, ChatMessage, LlmAgent, LlmModel, Project


class LlmModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LlmModel
        fields = ("id", "name", "description")


class LlmAgentSerializer(serializers.ModelSerializer):
    model = LlmModelSerializer(read_only=True)

    class Meta:
        model = LlmAgent
        fields = ("id", "name", "role", "context", "model")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "description")


class ProjectCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, default="")

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        if Project.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A project with this name already exists.")
        return value

    def validate_description(self, value: str) -> str:
        return value.strip()


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ("id", "role", "content", "created_at")


class ChatRequestSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField()
    prompt = serializers.CharField()
    event_id = serializers.CharField(max_length=64)
    agent_task_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_agent_id(self, value: int) -> int:
        if not LlmAgent.objects.filter(pk=value, active=True).exists():
            raise serializers.ValidationError("Active agent not found.")
        return value

    def validate_event_id(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Event ID is required.")
        return value

    def validate(self, data: dict) -> dict:
        agent_task_id = data.get("agent_task_id")
        if agent_task_id is not None:
            if not AgentTask.objects.filter(
                pk=agent_task_id,
                agent_id=data["agent_id"],
            ).exists():
                raise serializers.ValidationError(
                    {"agent_task_id": "Task not found for this agent."}
                )
        return data


class ChatHistoryRequestSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField()
    event_id = serializers.CharField(max_length=64)

    def validate_agent_id(self, value: int) -> int:
        if not LlmAgent.objects.filter(pk=value, active=True).exists():
            raise serializers.ValidationError("Active agent not found.")
        return value

    def validate_event_id(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Event ID is required.")
        return value


class ClearSessionSerializer(serializers.Serializer):
    event_id = serializers.CharField(max_length=64)

    def validate_event_id(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Event ID is required.")
        return value


class AgentTaskCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    project_id = serializers.IntegerField()

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_description(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Description is required.")
        return value

    def validate_project_id(self, value: int) -> int:
        if not Project.objects.filter(pk=value, active=True).exists():
            raise serializers.ValidationError("Active project not found.")
        return value


class AgentTaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = AgentTask
        fields = (
            "id",
            "agent",
            "project",
            "name",
            "vd_name",
            "description",
            "result",
            "vd_processed",
            "processed",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "agent",
            "project",
            "vd_name",
            "result",
            "vd_processed",
            "processed",
            "created_at",
            "updated_at",
        )
