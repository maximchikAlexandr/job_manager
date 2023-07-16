# Generated by Django 4.2 on 2023-07-16 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0005_budgetcalculation_calculation_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetcalculation',
            name='profit_percentage',
            field=models.PositiveIntegerField(default=25, null=True),
        ),
        migrations.AlterField(
            model_name='budgetcalculation',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
    ]