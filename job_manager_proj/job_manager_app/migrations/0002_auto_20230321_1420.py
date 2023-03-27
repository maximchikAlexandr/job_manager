# Generated by Django 4.1.7 on 2023-03-21 14:20
from django.conf import settings
from django.core.management import call_command
from django.db import migrations

from job_manager_app.apps import JobManagerAppConfig

fixture = settings.BASE_DIR / f"/job_manager_app/migrations/fixtures/dump.json"


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label=JobManagerAppConfig.name)

class Migration(migrations.Migration):

    dependencies = [
        ('job_manager_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
