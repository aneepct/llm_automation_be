from pathlib import Path

from django.core.management.base import BaseCommand

from llm.models import LlmAgent

PROMPT_FILE = Path(__file__).resolve().parents[2] / "prompts" / "product_manager_context.txt"
AGENT_NAME = "Product Manager"
ROLE = "Senior Product Manager"


class Command(BaseCommand):
    help = "Update Product Manager agent context with the latest PRD prompt (incl. Mermaid diagrams)."

    def handle(self, *args, **options):
        context = PROMPT_FILE.read_text(encoding="utf-8").strip()
        agent, created = LlmAgent.objects.update_or_create(
            name=AGENT_NAME,
            defaults={
                "role": ROLE,
                "context": context,
            },
        )
        verb = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{verb} agent '{agent.name}' (id={agent.pk})."))
