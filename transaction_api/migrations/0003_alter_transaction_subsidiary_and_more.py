# Generated by Django 4.0.5 on 2024-05-16 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction_api', '0002_alter_transaction_subsidiary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='subsidiary',
            field=models.CharField(choices=[('AMS', 'AMS'), ('ACS', 'ACS'), ('ASS', 'ASS'), ('APS', 'APS'), ('ATI', 'ATI')], max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('cash', 'Cash'), ('upi', 'UPI'), ('bank_transfer', 'Bank Transfer')], max_length=50),
        ),
        migrations.AlterModelTable(
            name='transaction',
            table='transactions',
        ),
    ]