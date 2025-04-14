# Generated by Django 5.0.6 on 2025-04-11 14:26

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0043_alter_acsparttimerstatus_date_happinessindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acsparttimerstatus',
            name='date',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date(2025, 4, 11))]),
        )
    ]
