# Generated by Django 4.0.5 on 2024-06-02 11:41

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('transaction_api', '0011_transaction_payment_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=22, unique=True),
        ),
    ]
