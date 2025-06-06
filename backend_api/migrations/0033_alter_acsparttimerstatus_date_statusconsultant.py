# Generated by Django 4.0.5 on 2024-10-20 09:43

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0032_alter_consultant_employer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acsparttimerstatus',
            name='date',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date(2024, 10, 20))]),
        ),
        migrations.CreateModel(
            name='StatusConsultant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('description', models.TextField(blank=True, null=True)),
                ('consultant_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='backend_api.consultant')),
                ('employer_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='backend_api.employer')),
                ('recruiter_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='backend_api.recruiter')),
            ],
            options={
                'db_table': 'status_consultant',
            },
        ),
    ]
