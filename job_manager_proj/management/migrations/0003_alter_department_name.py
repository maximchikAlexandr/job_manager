# Generated by Django 4.2 on 2023-07-01 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_alter_headofdepartment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]