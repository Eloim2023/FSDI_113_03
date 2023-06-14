# Generated by Django 4.2.2 on 2023-06-11 17:47

from django.db import migrations

def populate_status(apps, schemaeditor):
    entries = {
        "to-do":"Issue to do",
        "doing": "Issue currently on progress",
        "done": "Issue already done"
    }

    Status = apps.get_model("issues", "Status")
    for key, value in entries.items():
        status = Status(name=key, description=value)
        status.save()

def populate_priority(apps, schemaeditor):
    entries = {
        "low": "Low Priority",
        "medium": "Medium Priotity",
        "high": "High Priority"
    }

    Priority = apps.get_model("issues", "Priority")
    for key, value in entries.items():
        priority = Priority(name=key, description=value)
        priority.save()


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_status),
        migrations.RunPython(populate_priority)
    ]