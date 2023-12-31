# Generated by Django 4.0.5 on 2023-12-27 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0004_accessroles_name_of_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('full_name_verified', models.BooleanField(default=False)),
                ('phone_number', models.CharField(max_length=10)),
                ('email_id', models.EmailField(max_length=254)),
                ('dob', models.DateField()),
                ('visa_status', models.CharField(choices=[('OPT', 'OPT'), ('CPT', 'CPT'), ('H1B', 'H1B'), ('H4 EAD', 'H4 EAD')], max_length=20)),
                ('visa_status_verified', models.BooleanField(default=False)),
                ('visa_validity', models.DateField()),
                ('visa_validity_verified', models.BooleanField(default=False)),
                ('btech_college', models.CharField(max_length=100)),
                ('btech_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('btech_graduation_date', models.DateField()),
                ('masters_college', models.CharField(max_length=100)),
                ('masters_cgpa', models.DecimalField(decimal_places=2, max_digits=4)),
                ('masters_graduation_date', models.DateField()),
                ('technologies', models.JSONField()),
                ('current_location', models.CharField(max_length=100)),
                ('relocation', models.BooleanField()),
                ('experience_in_us', models.TextField()),
                ('experience_in_us_verified', models.BooleanField(default=False)),
                ('experience_in_india', models.TextField()),
                ('experience_in_india_verified', models.BooleanField(default=False)),
                ('relocation_preference', models.TextField()),
                ('passport_number', models.CharField(blank=True, max_length=50)),
                ('passport_number_verified', models.BooleanField(default=False)),
                ('driving_licence', models.CharField(blank=True, max_length=50)),
                ('rate_expectations', models.CharField(max_length=100)),
                ('last_4_ssn', models.CharField(max_length=4)),
                ('linkedin_url', models.URLField(blank=True)),
                ('original_resume', models.FileField(upload_to='resumes/')),
                ('consulting_resume', models.FileField(upload_to='resumes/')),
            ],
            options={
                'db_table': 'consultant_details',
            },
        ),
    ]
