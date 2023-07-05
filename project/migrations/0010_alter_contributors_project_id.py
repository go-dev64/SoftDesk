# Generated by Django 4.2.2 on 2023-07-05 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0009_rename_project_issues_project_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contributors",
            name="project_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_contributors",
                to="project.project",
            ),
        ),
    ]
