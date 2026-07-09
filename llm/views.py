import json

from django.http import JsonResponse, StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AgentTask, ChatMessage, LlmAgent, Project
from .serializers import (
    AgentTaskCreateSerializer,
    AgentTaskSerializer,
    ChatHistoryRequestSerializer,
    ChatMessageSerializer,
    ChatRequestSerializer,
    ClearSessionSerializer,
    LlmAgentSerializer,
    ProjectCreateSerializer,
    ProjectSerializer,
)
from .services import LlmAgentService
from .session import clear_session_messages, is_session_expired
from .task_processor import enqueue_agent_task


class ProjectListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        projects = Project.objects.filter(active=True).order_by("name")
        return Response(ProjectSerializer(projects, many=True).data)

    def post(self, request):
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.create(
            name=serializer.validated_data["name"],
            description=serializer.validated_data.get("description", ""),
        )
        return Response(ProjectSerializer(project).data, status=201)


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
        agent_task_id = serializer.validated_data.get("agent_task_id")

        def event_stream():
            payload = {
                "event_id": event_id,
                "agent_id": agent.id,
                "type": "start",
            }
            yield f"data: {json.dumps(payload)}\n\n"

            try:
                for chunk in LlmAgentService.run_stream(
                    agent,
                    prompt,
                    event_id,
                    agent_task_id=agent_task_id,
                ):
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


class AgentTaskListCreateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, agent_id: int):
        if not LlmAgent.objects.filter(pk=agent_id, active=True).exists():
            return Response({"detail": "Active agent not found."}, status=404)

        tasks = AgentTask.objects.filter(agent_id=agent_id).order_by("-created_at")
        return Response(AgentTaskSerializer(tasks, many=True).data)

    def post(self, request, agent_id: int):
        try:
            agent = LlmAgent.objects.get(pk=agent_id, active=True)
        except LlmAgent.DoesNotExist:
            return Response({"detail": "Active agent not found."}, status=404)

        serializer = AgentTaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = AgentTask.objects.create(
            agent=agent,
            project_id=serializer.validated_data["project_id"],
            name=serializer.validated_data["name"],
            description=serializer.validated_data["description"],
        )
        enqueue_agent_task(task.id)
        return Response(AgentTaskSerializer(task).data, status=201)


class AgentTaskDetailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, task_id: int):
        try:
            task = AgentTask.objects.get(pk=task_id)
        except AgentTask.DoesNotExist:
            return Response({"detail": "Task not found."}, status=404)

        return Response(AgentTaskSerializer(task).data)
