from django.urls import path

from .views import (
    AgentListView,
    AgentTaskDetailView,
    AgentTaskListCreateView,
    ChatHistoryView,
    ChatSessionClearView,
    ChatView,
    ProjectListView,
)

urlpatterns = [
    path("projects/", ProjectListView.as_view(), name="projects"),
    path("agents/", AgentListView.as_view(), name="agents"),
    path("agents/<int:agent_id>/tasks/", AgentTaskListCreateView.as_view(), name="agent-tasks"),
    path("tasks/<int:task_id>/", AgentTaskDetailView.as_view(), name="agent-task-detail"),
    path("chat/history/", ChatHistoryView.as_view(), name="chat-history"),
    path("chat/session/", ChatSessionClearView.as_view(), name="chat-session-clear"),
    path("chat/", ChatView.as_view(), name="chat"),
]
