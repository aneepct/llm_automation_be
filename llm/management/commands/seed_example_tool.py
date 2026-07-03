from django.core.management.base import BaseCommand

from llm.models import AgentTool
from llm.tools.generator import generate_tool_file
from llm.tools.registry import reload_registry

EXAMPLE_TOOL = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False,
    },
    "python_code": '''ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}
destination_city = kwargs["destination_city"]
price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
return f"The price of a ticket to {destination_city} is {price}"''',
}


class Command(BaseCommand):
    help = "Seed example get_ticket_price tool and generate its Python file."

    def handle(self, *args, **options):
        tool, created = AgentTool.objects.update_or_create(
            name=EXAMPLE_TOOL["name"],
            defaults={
                "description": EXAMPLE_TOOL["description"],
                "parameters": EXAMPLE_TOOL["parameters"],
                "python_code": EXAMPLE_TOOL["python_code"],
                "active": True,
            },
        )

        path = generate_tool_file(tool)
        reload_registry()

        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(f"{action} example tool and generated file at {path}")
        )
