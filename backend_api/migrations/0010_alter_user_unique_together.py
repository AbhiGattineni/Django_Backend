# Generated by Django 5.0.1 on 2024-01-29 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0009_parttimer_course_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('user_id',)},
        ),
    ]
