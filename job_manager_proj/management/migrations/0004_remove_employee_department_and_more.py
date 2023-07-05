# Generated by Django 4.2 on 2023-07-04 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0004_remove_agreementstage_service_agreement_and_more'),
        ('catalog', '0005_department_employee_headofdepartment_department_head'),
        ('management', '0003_alter_department_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='department',
        ),
        migrations.RemoveField(
            model_name='headofdepartment',
            name='employee',
        ),
        migrations.CreateModel(
            name='MonthProxy',
            fields=[
            ],
            options={
                'verbose_name': 'MonthJob - Month',
                'verbose_name_plural': 'MonthJobs - Months',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('catalog.month',),
        ),
        migrations.CreateModel(
            name='ServiceAgreementProxy',
            fields=[
            ],
            options={
                'verbose_name': 'MonthJob - Agreement',
                'verbose_name_plural': 'MonthJobs - Agreements',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('commerce.serviceagreement',),
        ),
        migrations.AlterField(
            model_name='monthjob',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='catalog.employee'),
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='HeadOfDepartment',
        ),
    ]
