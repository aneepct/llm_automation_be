import json

from django.http import JsonResponse, StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatMessage, LlmAgent
from .serializers import (
    ChatHistoryRequestSerializer,
    ChatMessageSerializer,
    ChatRequestSerializer,
    ClearSessionSerializer,
    LlmAgentSerializer,
)
from .services import LlmAgentService
from .session import clear_session_messages, is_session_expired


class AgentListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        agents = LlmAgent.objects.filter(active=True).select_related("model")
        return Response(LlmAgentSerializer(agents, many=True).data)


class ChatHistoryView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        serializer = ChatHistoryRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        event_id = serializer.validated_data["event_id"]
        if is_session_expired(event_id):
            clear_session_messages(event_id)
            return Response([])

        messages = ChatMessage.objects.filter(
            event_id=event_id,
            agent_id=serializer.validated_data["agent_id"],
        ).order_by("created_at")

        return Response(ChatMessageSerializer(messages, many=True).data)


@method_decorator(csrf_exempt, name="dispatch")
class ChatSessionClearView(View):
    def delete(self, request):
        try:
            data = json.loads(request.body.decode("utf-8") or "{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"detail": "Invalid JSON body."}, status=400)

        serializer = ClearSessionSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        event_id = serializer.validated_data["event_id"]
        deleted = clear_session_messages(event_id)
        return JsonResponse({"event_id": event_id, "deleted": deleted})


@method_decorator(csrf_exempt, name="dispatch")
class ChatView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"detail": "Invalid JSON body."}, status=400)

        serializer = ChatRequestSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        event_id = serializer.validated_data["event_id"]

        if is_session_expired(event_id):
            clear_session_messages(event_id)
            return JsonResponse(
                {"detail": "Session expired. Start a new session."},
                status=410,
            )

        agent = LlmAgent.objects.select_related("model").get(
            pk=serializer.validated_data["agent_id"]
        )
        prompt = serializer.validated_data["prompt"]

        def event_stream():
            payload = {
                "event_id": event_id,
                "agent_id": agent.id,
                "type": "start",
            }
            yield f"data: {json.dumps(payload)}\n\n"

            try:
                for chunk in LlmAgentService.run_stream(agent, prompt, event_id):
                    payload = {
                        "event_id": event_id,
                        "agent_id": agent.id,
                        "type": "chunk",
                        "content": chunk,
                    }
                    yield f"data: {json.dumps(payload)}\n\n"
            except Exception as exc:
                payload = {
                    "event_id": event_id,
                    "agent_id": agent.id,
                    "type": "error",
                    "error": str(exc),
                }
                yield f"data: {json.dumps(payload)}\n\n"
                return

            payload = {
                "event_id": event_id,
                "agent_id": agent.id,
                "type": "done",
            }
            yield f"data: {json.dumps(payload)}\n\n"

        response = StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response
