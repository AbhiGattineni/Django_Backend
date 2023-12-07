from django.db import models
from django.contrib.auth.models import User

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