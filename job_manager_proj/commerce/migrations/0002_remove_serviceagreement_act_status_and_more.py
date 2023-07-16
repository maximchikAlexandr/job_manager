# Generated by Django 4.2 on 2023-07-15 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceagreement',
            name='act_status',
        ),
        migrations.RemoveField(
            model_name='serviceagreement',
            name='month_of_accounting_act_in_salary',
        ),
        migrations.RemoveField(
            model_name='serviceagreement',
            name='month_signing_the_act',
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='accident_insurance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='depreciation_expenses',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='income_taxes',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='overhead_expenses',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='price_excluding_vat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='social_security_contributions',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='transportation_expenses',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='budgetcalculation',
            name='travel_expenses',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=14),
        ),
        migrations.AddField(
            model_name='commercialproposal',
            name='advance_payment_deadline',
            field=models.PositiveIntegerField(default=15),
        ),
        migrations.AddField(
            model_name='commercialproposal',
            name='advance_payment_percentage',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AddField(
            model_name='commercialproposal',
            name='payment_deferral',
            field=models.PositiveIntegerField(default=30),
        ),
    ]