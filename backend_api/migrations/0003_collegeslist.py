# Generated by Django 5.0.1 on 2024-01-22 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0002_delete_collegeslist'),
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
                ('application_UG_fee_link', models.URLField(blank=True, null=True)),
                ('application_graduation_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('application_graduation_fee_link', models.URLField(blank=True, null=True)),
                ('gre_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('gre_score_link', models.URLField(blank=True, null=True)),
                ('toefl_UG_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('toefl_UG_score_link', models.URLField(blank=True, null=True)),
                ('toefl_graduation_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('toefl_graduation_score_link', models.URLField(blank=True, null=True)),
                ('ielts_ug_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ielts_ug_score_link', models.URLField(blank=True, null=True)),
                ('ielts_graduation_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('ielts_graduation_score_link', models.URLField(blank=True, null=True)),
                ('fall_deadline_UG', models.DateField(blank=True, null=True)),
                ('fall_deadline_UG_link', models.URLField(blank=True, null=True)),
                ('fall_deadline_graduation', models.DateField(blank=True, null=True)),
                ('fall_deadline_graduation_link', models.URLField(blank=True, null=True)),
                ('spring_deadline_UG', models.DateField(blank=True, null=True)),
                ('spring_deadline_UG_link', models.URLField(blank=True, null=True)),
                ('spring_deadline_graduation', models.DateField(blank=True, null=True)),
                ('spring_deadline_graduation_link', models.URLField(blank=True, null=True)),
                ('college_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('college_email_link', models.URLField(blank=True, null=True)),
                ('college_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('college_phone_link', models.URLField(blank=True, null=True)),
                ('international_person_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('international_person_email_link', models.URLField(blank=True, null=True)),
                ('public_private', models.CharField(blank=True, choices=[('public', 'Public'), ('private', 'Private')], max_length=10, null=True)),
                ('UG_courses', models.TextField(blank=True, null=True)),
                ('UG_courses_link', models.URLField(blank=True, null=True)),
                ('graduation_courses', models.TextField(blank=True, null=True)),
                ('graduation_courses_link', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'collegelist',
            },
        ),
    ]
