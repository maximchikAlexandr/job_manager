# Generated by Django 4.2 on 2023-07-15 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signatory',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
