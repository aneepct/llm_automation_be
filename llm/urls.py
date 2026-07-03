from django.urls import path

from .views import AgentListView, ChatHistoryView, ChatSessionClearView, ChatView

urlpatterns = [
    path("agents/", AgentListView.as_view(), name="agents"),
    path("chat/history/", ChatHistoryView.as_view(), name="chat-history"),
    path("chat/session/", ChatSessionClearView.as_view(), name="chat-session-clear"),
    path("chat/", ChatView.as_view(), name="chat"),
]
