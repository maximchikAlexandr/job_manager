# Generated by Django 4.2 on 2023-07-01 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_alter_actofcompletedwork_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commercialproposal',
            name='type_of_jobs',
        ),
        migrations.RemoveField(
            model_name='serviceagreement',
            name='company',
        ),
    ]
