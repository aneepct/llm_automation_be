from django.core.management.base import BaseCommand

from llm.models import LlmModel

DEFAULT_MODELS = [
    {
        "name": "gpt-5-nano",
        "description": "OpenAI GPT-5 Nano — fast, low-cost model for simple tasks.",
    },
    {
        "name": "gpt-4o",
        "description": "OpenAI GPT-4o — multimodal flagship model.",
    },
    {
        "name": "gpt-4o-mini",
        "description": "OpenAI GPT-4o Mini — affordable, capable everyday model.",
    },
    {
        "name": "llama3.2",
        "description": "Meta Llama 3.2 — local model via Ollama.",
    },
    {
        "name": "gemini-2.0-flash",
        "description": "Google Gemini 2.0 Flash — fast Gemini model via OpenAI-compatible API.",
    },
]


class Command(BaseCommand):
    help = "Seed default LLM models available for agents."

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for entry in DEFAULT_MODELS:
            _, created = LlmModel.objects.update_or_create(
                name=entry["name"],
                defaults={
                    "description": entry["description"],
                    "active": True,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded LLM models: {created_count} created, {updated_count} updated."
            )
        )
