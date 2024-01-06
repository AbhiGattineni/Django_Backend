# Generated by Django 4.0.5 on 2023-12-24 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollegesList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(max_length=255)),
                ('website_link', models.URLField(blank=True, null=True)),
                ('international_UG_link', models.URLField(blank=True, null=True)),
                ('international_graduation_link', models.URLField(blank=True, null=True)),
                ('application_UG_link', models.URLField(blank=True, null=True)),
                ('application_graduation_link', models.URLField(blank=True, null=True)),
                ('application_UG_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('application_graduation_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('gre_score', models.PositiveIntegerField(blank=True, null=True)),
                ('toefl_UG_score', models.PositiveIntegerField(blank=True, null=True)),
                ('toefl_graduation_score', models.PositiveIntegerField(blank=True, null=True)),
                ('fall_deadline_UG', models.DateField(blank=True, null=True)),
                ('fall_deadline_graduation', models.DateField(blank=True, null=True)),
                ('spring_deadline_UG', models.DateField(blank=True, null=True)),
                ('spring_deadline_graduation', models.DateField(blank=True, null=True)),
                ('ielts_ug_score', models.PositiveIntegerField(blank=True, null=True)),
                ('ielts_graduation_score', models.PositiveIntegerField(blank=True, null=True)),
                ('college_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('college_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('international_person_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('public_private', models.CharField(blank=True, choices=[('public', 'Public'), ('private', 'Private')], max_length=10, null=True)),
                ('UG_courses', models.TextField(blank=True, null=True)),
                ('graduation_courses', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'collegelist',
            },
        ),
        migrations.CreateModel(
            name='PartTimer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('referred_by', models.CharField(blank=True, max_length=255, null=True)),
                ('current_occupation', models.CharField(max_length=255)),
                ('is_student', models.BooleanField(default=False)),
                ('course_of_study', models.CharField(blank=True, max_length=255, null=True)),
                ('current_pursuing_year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('role_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'role',
            },
        ),
    ]