from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import ChatMessage


def get_session_ttl() -> timedelta:
    return timedelta(hours=settings.CHAT_SESSION_TTL_HOURS)


def is_session_expired(event_id: str) -> bool:
    last_message = (
        ChatMessage.objects.filter(event_id=event_id)
        .order_by("-created_at")
        .first()
    )
    if not last_message:
        return False

    return last_message.created_at < timezone.now() - get_session_ttl()


def clear_session_messages(event_id: str) -> int:
    deleted, _ = ChatMessage.objects.filter(event_id=event_id).delete()
    return deleted
