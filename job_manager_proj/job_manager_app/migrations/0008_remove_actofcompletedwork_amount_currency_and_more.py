# Generated by Django 4.1.7 on 2023-03-21 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_manager_app', '0007_alter_actofcompletedwork_month_of_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actofcompletedwork',
            name='amount_currency',
        ),
        migrations.RemoveField(
            model_name='serviceagreement',
            name='amount_currency',
        ),
        migrations.AlterField(
            model_name='actofcompletedwork',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=14),
        ),
        migrations.AlterField(
            model_name='serviceagreement',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=14),
        ),
    ]
