from django.core.management.base import BaseCommand, CommandError

from llm.models import AgentTask, LlmAgent
from llm.vector_store import clear_agent_collection, reindex_agent_task


class Command(BaseCommand):
    help = "Re-index vector DB documents for an agent's processed tasks."

    def add_arguments(self, parser):
        parser.add_argument("--agent-id", type=int, required=True)
        parser.add_argument(
            "--clear-first",
            action="store_true",
            help="Clear the agent vector collection before re-indexing.",
        )

    def handle(self, *args, **options):
        agent_id = options["agent_id"]
        if not LlmAgent.objects.filter(pk=agent_id).exists():
            raise CommandError(f"Agent {agent_id} not found.")

        if options["clear_first"]:
            deleted = clear_agent_collection(agent_id)
            self.stdout.write(f"Cleared {deleted} vector(s).")

        tasks = AgentTask.objects.filter(agent_id=agent_id).select_related("project")
        if not tasks.exists():
            self.stdout.write("No tasks found for this agent.")
            return

        count = 0
        for task in tasks:
            reindex_agent_task(task)
            count += 1
            self.stdout.write(f"Re-indexed task {task.id}: {task.name}")

        self.stdout.write(self.style.SUCCESS(f"Re-indexed {count} task(s) for agent {agent_id}."))
