# Generated by Django 4.0.5 on 2024-12-31 12:42

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0037_teammember_consultant_uploaded_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultant',
            name='btech_college',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='btech_graduation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='btech_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='last_4_ssn',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='masters_cgpa',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='masters_college',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='masters_graduation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='rate_expectations',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='relocation_preference',
            field=models.TextField(blank=True, null=True),
        ),
    ]