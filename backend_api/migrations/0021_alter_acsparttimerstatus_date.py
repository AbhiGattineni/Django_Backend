# Generated by Django 4.0.5 on 2024-05-19 11:31

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0020_alter_acsparttimerstatus_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acsparttimerstatus',
            name='date',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date(2024, 5, 19))]),
        ),
    ]
