# Generated by Django 5.0.1 on 2024-01-22 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0004_alter_collegeslist_application_ug_fee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegeslist',
            name='fall_deadline_UG',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='collegeslist',
            name='fall_deadline_graduation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='collegeslist',
            name='spring_deadline_UG',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='collegeslist',
            name='spring_deadline_graduation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
