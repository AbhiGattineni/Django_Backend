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

class Consultant(models.Model):
    name = models.CharField(max_length=100)
    fullName = models.CharField(max_length=200, default='N/A')  # default value
    visaStatus = models.CharField(max_length=100, default='N/A')  # default value
    college = models.CharField(max_length=100, default='N/A')  # default value
    technology = models.CharField(max_length=100, default='N/A')  # default value
    dob = models.DateField(default=date.today)  # default to current date
    originalResume = models.URLField(blank=True)  # Assuming it's a URL
    title = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        db_table = 'consultants'

    def __str__(self):
        return self.name