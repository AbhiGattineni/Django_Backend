# Generated by Django 4.0.5 on 2024-06-02 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0023_statusupdates_alter_acsparttimerstatus_date'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='statusupdates',
            table='Status_updates',
        ),
    ]