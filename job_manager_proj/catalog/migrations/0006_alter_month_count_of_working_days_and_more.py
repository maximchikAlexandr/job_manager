# Generated by Django 4.2 on 2023-07-08 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_department_employee_headofdepartment_department_head'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='count_of_working_days',
            field=models.PositiveIntegerField(),
        ),
        migrations.AddConstraint(
            model_name='month',
            constraint=models.CheckConstraint(check=models.Q(('count_of_working_days__lte', 31)), name='month_count_of_working_days_check'),
        ),
    ]
