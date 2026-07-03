from rest_framework import serializers

from .models import ChatMessage, LlmAgent, LlmModel


class LlmModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LlmModel
        fields = ("id", "name", "description")


class LlmAgentSerializer(serializers.ModelSerializer):
    model = LlmModelSerializer(read_only=True)

    class Meta:
        model = LlmAgent
        fields = ("id", "name", "role", "context", "model")


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ("id", "role", "content", "created_at")


class ChatRequestSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField()
    prompt = serializers.CharField()
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
