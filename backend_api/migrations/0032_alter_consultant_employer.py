# Generated by Django 4.0.5 on 2024-10-17 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0031_employer_recruiter_remove_shopingproduct_image_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultant',
            name='employer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend_api.employer'),
        ),
    ]
