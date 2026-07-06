import logging
import threading

from django.db import transaction

from .models import AgentTask
from .services import LlmAgentService
from .vector_store import (
    ingest_project_record,
    ingest_task_description,
    ingest_task_result,
    rebuild_project_catalog,
)

logger = logging.getLogger(__name__)


def enqueue_agent_task(task_id: int) -> None:
    transaction.on_commit(
        lambda: threading.Thread(
            target=process_agent_task,
            args=(task_id,),
            daemon=True,
        ).start()
    )


def process_agent_task(task_id: int) -> None:
    try:
        task = AgentTask.objects.select_related(
            "agent",
            "agent__model",
            "project",
        ).get(pk=task_id)
    except AgentTask.DoesNotExist:
        logger.error("AgentTask %s not found", task_id)
        return

    agent = task.agent

    try:
        ingest_project_record(agent_id=agent.id, project=task.project)
        rebuild_project_catalog(agent_id=agent.id)

        result = LlmAgentService.run_task(
            agent,
            task.description,
            project_id=task.project_id,
            exclude_task_id=task.id,
        )
        task.result = result
        task.save(update_fields=["result", "updated_at"])

        ingest_task_description(task=task)
        task.vd_processed = True
        task.save(update_fields=["vd_processed", "updated_at"])

        ingest_task_result(task=task)
        task.processed = True
        task.save(update_fields=["processed", "updated_at"])
    except Exception:
        logger.exception("Failed to process AgentTask %s", task_id)
