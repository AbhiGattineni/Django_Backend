from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Todo(models.Model):
    task = models.CharField(max_length = 180)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    completed = models.BooleanField(default = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.task

class Person(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PartTimer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    referred_by = models.CharField(max_length=255, blank=True, null=True) 
    current_occupation = models.CharField(max_length=255)
    is_student = models.BooleanField(default=False)  
    course_of_study = models.CharField(max_length=255, blank=True, null=True)  
    current_pursuing_year = models.IntegerField(blank=True, null=True)  

    def __str__(self):
        return self.name
class Role(models.Model):
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    role_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'role'
    def _str_(self):
        return self.user_id

class CollegesList(models.Model):
    college_name = models.CharField(max_length=255)
    website_link = models.URLField(blank=True, null=True)
    international_UG_link = models.URLField(blank=True, null=True)
    international_graduation_link = models.URLField(blank=True, null=True)
    application_UG_link = models.URLField(blank=True, null=True)
    application_graduation_link = models.URLField(blank=True, null=True)
    application_UG_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    application_graduation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gre_score = models.PositiveIntegerField(blank=True, null=True)
    toefl_UG_score = models.PositiveIntegerField(blank=True, null=True)
    toefl_graduation_score = models.PositiveIntegerField(blank=True, null=True)
    fall_deadline_UG = models.DateField(blank=True, null=True)
    fall_deadline_graduation = models.DateField(blank=True, null=True)
    spring_deadline_UG = models.DateField(blank=True, null=True)
    spring_deadline_graduation = models.DateField(blank=True, null=True)
    ielts_ug_score = models.PositiveIntegerField(blank=True, null=True)
    ielts_graduation_score = models.PositiveIntegerField(blank=True, null=True)
    college_email = models.EmailField(blank=True, null=True)
    college_phone = models.CharField(max_length=15, blank=True, null=True)
    international_person_email = models.EmailField(blank=True, null=True)
    public_private = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')], blank=True, null=True)
    UG_courses = models.TextField(blank=True, null=True)
    graduation_courses = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'collegelist'
    def _str_(self):
        return self.college_name

class AccessRoles(models.Model):
    admin_access_role = models.CharField(max_length=255)
    name_of_role = models.CharField(max_length=255,default='role_name')

    def __str__(self):
        return self.admin_access_role

    class Meta:
        db_table = 'access_roles'


class Consultant(models.Model):
    # Basic Information
    full_name = models.CharField(max_length=100)
    full_name_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10)  # Assuming only digits, no formatting
    email_id = models.EmailField()
    dob = models.DateField()  # Date of Birth
    visa_status = models.CharField(max_length=20, choices=[
        ('OPT', 'OPT'), 
        ('CPT', 'CPT'), 
        ('H1B', 'H1B'), 
        ('H4 EAD', 'H4 EAD')
    ])
    visa_status_verified = models.BooleanField(default=False)
    visa_validity = models.DateField()
    visa_validity_verified = models.BooleanField(default=False)

    # Education Details
    btech_college = models.CharField(max_length=100)
    btech_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    btech_graduation_date = models.DateField()
    masters_college = models.CharField(max_length=100)
    masters_cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    masters_graduation_date = models.DateField()

    # Professional Details
    technologies = models.JSONField()  # Storing an array of strings
    current_location = models.CharField(max_length=100)
    relocation = models.BooleanField()
    experience_in_us = models.TextField()  # To store detailed text
    experience_in_us_verified = models.BooleanField(default=False)
    experience_in_india = models.TextField()  # To store detailed text
    experience_in_india_verified = models.BooleanField(default=False)
    relocation_preference = models.TextField()  # Cities and states

    # Personal Details
    passport_number = models.CharField(max_length=50, blank=True)
    passport_number_verified = models.BooleanField(default=False)
    driving_licence = models.CharField(max_length=50, blank=True)
    rate_expectations = models.CharField(max_length=100)
    last_4_ssn = models.CharField(max_length=4)
    linkedin_url = models.URLField(max_length=200, blank=True)

    # Resume Fields
    original_resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    consulting_resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'consultant_details'

