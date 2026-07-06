from django.db import migrations, models
import django.db.models.deletion


def create_default_project(apps, schema_editor):
    Project = apps.get_model("llm", "Project")
    AgentTask = apps.get_model("llm", "AgentTask")
    project, _ = Project.objects.get_or_create(
        name="Unassigned",
        defaults={"description": "Default project for tasks created before projects were introduced."},
    )
    AgentTask.objects.filter(project__isnull=True).update(project=project)


class Migration(migrations.Migration):
    dependencies = [
        ("llm", "0004_agenttask"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="agenttask",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tasks",
                to="llm.project",
            ),
        ),
        migrations.RunPython(create_default_project, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="agenttask",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tasks",
                to="llm.project",
            ),
        ),
    ]
