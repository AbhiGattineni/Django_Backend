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
