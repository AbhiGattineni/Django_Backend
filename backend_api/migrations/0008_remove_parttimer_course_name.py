# Generated by Django 5.0.1 on 2024-01-29 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0007_remove_user_id_alter_user_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parttimer',
            name='course_name',
        ),
    ]
