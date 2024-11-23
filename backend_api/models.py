from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MaxValueValidator
from django.utils import timezone

def current_date():
    return timezone.now().date()

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
    user = models.CharField(null=True, blank=True,max_length=100)
    answered_questions = models.BooleanField(default=False)
    current_occupation = models.CharField(max_length=100)
    year_of_study = models.CharField(max_length=100, null=True, blank=True)  # Nullable, as it's conditional
    course_name = models.CharField(max_length=100, null=True, blank=True)  # Nullable
    referred_by = models.CharField(max_length=100, null=True, blank=True)  # Assuming this could be nullable

    class Meta:
        db_table = 'PartTimer'

    def __str__(self):
        return f"{self.user.full_name} - {self.current_occupation}"


class Role(models.Model):
    user_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    role_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'role'
    def __str__(self):
        return self.user_id

class CollegesList(models.Model):
    college_name = models.CharField(max_length=255)
    website_link = models.URLField(blank=True, null=True)
    international_UG_link = models.URLField(blank=True, null=True)
    international_graduation_link = models.URLField(blank=True, null=True)
    application_UG_link = models.URLField(blank=True, null=True)
    application_graduation_link = models.URLField(blank=True, null=True)
    application_UG_fee = models.TextField(blank=True, null=True)
    application_UG_fee_link = models.URLField(blank=True, null=True)
    application_graduation_fee = models.TextField(blank=True, null=True)
    application_graduation_fee_link = models.URLField(blank=True, null=True)
    gre_score = models.TextField(blank=True, null=True)
    gre_score_link = models.URLField(blank=True, null=True)
    toefl_UG_score = models.TextField(blank=True, null=True)
    toefl_UG_score_link = models.URLField(blank=True, null=True)
    toefl_graduation_score = models.TextField(blank=True, null=True)
    toefl_graduation_score_link = models.URLField(blank=True, null=True)
    ielts_ug_score = models.TextField(blank=True, null=True)
    ielts_ug_score_link = models.URLField(blank=True, null=True)
    ielts_graduation_score = models.TextField(blank=True, null=True)
    ielts_graduation_score_link = models.URLField(blank=True, null=True)
    fall_deadline_UG = models.TextField(blank=True, null=True)
    fall_deadline_UG_link = models.URLField(blank=True, null=True)
    fall_deadline_graduation = models.TextField(blank=True, null=True)
    fall_deadline_graduation_link = models.URLField(blank=True, null=True)
    spring_deadline_UG = models.TextField(blank=True, null=True)
    spring_deadline_UG_link = models.URLField(blank=True, null=True)
    spring_deadline_graduation = models.TextField(blank=True, null=True)
    spring_deadline_graduation_link = models.URLField(blank=True, null=True)
    college_email = models.EmailField(blank=True, null=True)
    college_email_link = models.URLField(blank=True, null=True)
    college_phone = models.CharField(max_length=15, blank=True, null=True)
    college_phone_link = models.URLField(blank=True, null=True)
    international_person_email = models.EmailField(blank=True, null=True)
    international_person_email_link = models.URLField(blank=True, null=True)
    public_private = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')], blank=True, null=True)
    UG_courses = models.TextField(blank=True, null=True)
    UG_courses_link = models.URLField(blank=True, null=True)
    graduation_courses = models.TextField(blank=True, null=True)
    graduation_courses_link = models.URLField(blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'collegelist'

    def __str__(self):
        return self.college_name

class CollegeDetail(models.Model):
    college = models.ForeignKey(CollegesList, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=255, null=False, blank=False)
    label = models.CharField(max_length=255, null=False, blank=False)
    link = models.URLField()

    class Meta:
        db_table = 'social_links'

    def __str__(self):
        return self.college_name

class AccessRoles(models.Model):
    admin_access_role = models.CharField(max_length=255)
    name_of_role = models.CharField(max_length=255,default='role_name')

    def __str__(self):
        return self.admin_access_role

    class Meta:
        db_table = 'access_roles'


class Employer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'employer_details'

class Recruiter(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)
    employer = models.CharField(max_length=255)  # Employer name as a string field
    email = models.EmailField()

    def __str__(self):
        return f'{self.name} ({self.employer})'
    
    class Meta:
        db_table = 'recrutier_details'

class Consultant(models.Model):
    # Foreign Keys
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='consultant_employers', null=True)
    recruiter_id = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='consultant_recruiters', null=True)

    # Basic Information
    full_name = models.CharField(max_length=100)
    full_name_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, unique=True)
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

    # Resume Fields add
    original_resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    consulting_resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'consultant_details'

class StatusConsultant(models.Model):
    consultant_id = models.ForeignKey(Consultant, on_delete=models.CASCADE, default=None)
    recruiter_id = models.ForeignKey(Recruiter, on_delete=models.CASCADE, default=None)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE, default=None)
    date = models.DateField(default=timezone.now)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Note on {self.date} is {self.description}'
    
    class Meta:
        db_table = 'status_consultant'

class User(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_country_code = models.CharField(max_length=4, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    email_id = models.EmailField()
    enrolled_services = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'User'
        # Specify that 'user_id' is the primary key
        unique_together = (("user_id",),)

    def __str__(self):
        return self.user_id

class Package(models.Model):
    package_name = models.CharField(max_length=100)
    includes = models.JSONField(default=list)  # Array of strings
    excludes = models.JSONField(default=list)  # Array of strings
    package_for = models.CharField(max_length=100)

    class Meta:
        db_table = 'Packages'

    def __str__(self):
        return self.package_name

class AcsParttimerStatus(models.Model):
    parttimerName = models.CharField(max_length=100, blank=False)
    parttimerId = models.CharField(max_length=100, blank=False)
    studentName = models.CharField(max_length=100, blank=False)
    studentId = models.CharField(max_length=100)
    date = models.DateField(blank=False, validators=[MaxValueValidator(timezone.now().date())])
    applicationsAppliedSearched = models.IntegerField(default=0)
    applicationsAppliedSaved = models.IntegerField(default=0)
    easyApply = models.IntegerField(default=0)
    recruiterDirectMessages = models.CharField(max_length=200, blank=True, null=True)
    connectMessages = models.CharField(max_length=200, blank=True, null=True)
    reason = models.CharField(max_length=500, blank=True, null=True)
    description= models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'PartTimer_status'

    def __str__(self):
        return f"{self.parttimerName}'s Application on {self.date}"


class StatusUpdates(models.Model):
    user_id = models.CharField(max_length=100, blank=False)
    user_name = models.CharField(max_length=100, blank=False)
    date = models.DateField(blank=False, validators=[MaxValueValidator(current_date)])
    status = models.CharField(max_length=100, blank=False)

    class Meta:
        db_table = 'Status_updates'

    def __str__(self):
        return f"{self.user_name}'s status added on {self.date}"
    
from django.db import models

class ShopingProduct(models.Model):
    name = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='products/', blank=False, null=True)  # Use ImageField here
    link = models.URLField(max_length=200, blank=False)
    age_group = models.CharField(max_length=20, blank=False)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'ShopingProduct'

    def __str__(self):
        return f"{self.name}"


class TeamMember(models.Model):
    name = models.CharField(max_length=100, blank=False)
    work_time_from = models.DateField(blank=False,null=True)  # Starting date of work
    work_time_to = models.DateField(blank=False,null=True)    # Ending date of work
    role = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)  # Description of the person
    image = models.ImageField(upload_to='team_members/', blank=False, null=True)  # ImageField for the person's image
    facebook_link = models.URLField(max_length=200, blank=True)  # Facebook page link
    linkedin_link = models.URLField(max_length=200, blank=True)  # LinkedIn page link
    github_link = models.URLField(max_length=200, blank=True)  # GitHub page link
    subsidiary = models.CharField(max_length=100, blank=False)  # Subsidiary name
    

    class Meta:
        db_table = 'team_member'

    def __str__(self):
        return f"{self.name}"
