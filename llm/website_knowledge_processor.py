import logging
import threading

from django.db import transaction

from .models import WebsiteKnowledgeJob
from .scraper import fetch_website_contents
from .services import LlmAgentService
from .vector_store import ingest_admin_knowledge
from .website_knowledge import (
    is_usable_content,
    parse_page_body,
    parse_page_title,
    website_source_id,
)

logger = logging.getLogger(__name__)

MAX_CHARS_PER_PAGE = 50_000


def enqueue_website_knowledge_job(job_id: int) -> None:
    transaction.on_commit(
        lambda: threading.Thread(
            target=process_website_knowledge_job,
            args=(job_id,),
            daemon=True,
        ).start()
    )


def process_website_knowledge_job(job_id: int) -> None:
    try:
        job = WebsiteKnowledgeJob.objects.select_related(
            "agent",
            "agent__model",
        ).get(pk=job_id)
    except WebsiteKnowledgeJob.DoesNotExist:
        logger.error("WebsiteKnowledgeJob %s not found", job_id)
        return

    job.status = WebsiteKnowledgeJob.Status.RUNNING
    job.save(update_fields=["status", "updated_at"])

    ingested_count = 0
    errors: list[str] = []

    for url in job.selected_urls:
        try:
            raw_content = fetch_website_contents(url, max_chars=MAX_CHARS_PER_PAGE)
            if not is_usable_content(raw_content):
                errors.append(
                    f"Skipped {url}: insufficient or invalid content "
                    f"({raw_content[:120]!r})"
                )
                job.completed_count += 1
                job.save(update_fields=["completed_count", "updated_at"])
                continue

            title = parse_page_title(raw_content)
            body = parse_page_body(raw_content)
            text = body

            if job.use_llm_cleanup:
                try:
                    text = LlmAgentService.clean_website_content(
                        job.agent,
                        raw_content,
                        url,
                    )
                except Exception as exc:
                    logger.warning("LLM cleanup failed for %s: %s", url, exc)
                    errors.append(f"LLM cleanup failed for {url}, using raw text")

            if not text.strip():
                errors.append(f"Skipped {url}: empty content after cleanup")
                job.completed_count += 1
                job.save(update_fields=["completed_count", "updated_at"])
                continue

            ingest_admin_knowledge(
                agent_id=job.agent_id,
                title=title,
                text=text,
                source_id=website_source_id(url),
                source_url=url,
            )
            ingested_count += 1
        except Exception as exc:
            logger.exception("Failed to ingest %s for job %s", url, job_id)
            errors.append(f"Failed {url}: {exc}")
        finally:
            job.completed_count += 1
            job.save(update_fields=["completed_count", "updated_at"])

    if ingested_count == 0:
        job.status = WebsiteKnowledgeJob.Status.FAILED
    else:
        job.status = WebsiteKnowledgeJob.Status.COMPLETED

    if errors:
        job.error_message = "\n".join(errors)
    job.save(update_fields=["status", "error_message", "updated_at"])
