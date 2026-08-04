#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

SKIP_AUTO_MIGRATE = {
    "migrate",
    "makemigrations",
    "showmigrations",
    "sqlmigrate",
    "squashmigrations",
    "optimizemigration",
}


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import call_command, execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    if command == "runserver" and len(sys.argv) == 2:
        sys.argv.append("0.0.0.0:8000")
    if command not in SKIP_AUTO_MIGRATE:
        import django

        django.setup()
        call_command("migrate", verbosity=0, interactive=False)

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
