# Generated by Django 4.0.5 on 2024-10-21 17:01

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0033_alter_acsparttimerstatus_date_statusconsultant'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultant',
            name='employer_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultant_employers', to='backend_api.employer'),
        ),
        migrations.AddField(
            model_name='consultant',
            name='recruiter_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultant_recruiters', to='backend_api.recruiter'),
        ),
        migrations.AlterField(
            model_name='acsparttimerstatus',
            name='date',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date(2024, 10, 21))]),
        ),
    ]
