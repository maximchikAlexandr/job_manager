# Generated by Django 4.2 on 2023-07-15 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_remove_serviceagreement_act_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetcalculation',
            name='vat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
    ]
