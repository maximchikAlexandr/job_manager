# Generated by Django 4.2 on 2023-07-03 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_month_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='bank_name',
            field=models.CharField(max_length=50),
        ),
    ]
