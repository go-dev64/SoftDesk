# Generated by Django 4.2.2 on 2023-06-28 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0002_rename_author_user_id_comments_author_user_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comments",
            old_name="author_user",
            new_name="author_user_id",
        ),
        migrations.RenameField(
            model_name="issues",
            old_name="author_user",
            new_name="author_user_id",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="author_user",
            new_name="author_user_id",
        ),
    ]
