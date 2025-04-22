from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=250)
    objective = models.TextField(blank=True)

    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.profile_id)

class Skills(models.Model):
    skill_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.category}"

class AdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='additional_info')

    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=False, blank=False)
    languages_known = models.CharField(max_length=255)

    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    location = models.CharField(max_length=255)

    github_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
    portfolio_url = models.URLField(max_length=255, null=True, blank=True)

    skills = models.ManyToManyField(Skills, blank=True, related_name='profile_skills')

    achievements = models.TextField(null=True, blank=True)

    resume_file = models.FileField(upload_to='own_resumes/', null=True, blank=True)

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)

    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.institution}"

class Experiences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100, choices=[('industry', 'Industry Based Project Experience'), ('non_academic', 'Non-Academic Projects'), ('academic', 'Academic Projects')], default='academic')
    
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    skills = models.ManyToManyField(Skills, related_name='projects')
    live_url = models.URLField(max_length=255, null=True, blank=True)
    github_repo_url = models.URLField(max_length=255, null=True, blank=True)

    cover_image = models.ImageField(upload_to='project_covers/', blank=True, null=True)

    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.title}"

class ResumeTemplates(models.Model):
    name = models.CharField(max_length=255)
    html_file = models.FileField(upload_to='resume_templates/template/html/')
    css_file = models.FileField(upload_to='resume_templates/template/css/')
    preview_image = models.ImageField(upload_to='resume_templates/previews/')
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.name

class Resumes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(ResumeTemplates, on_delete=models.SET_NULL, null=True, blank=True)

    resume_id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=250, null=True, blank=True)
    roll_number = models.CharField(max_length=50, null=True, blank=True)
    objective = models.TextField()
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    languages_known = models.CharField(max_length=255, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    github_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
    portfolio_url = models.URLField(max_length=255, null=True, blank=True)

    skills = models.ManyToManyField(Skills, related_name='resume_skills')

    selected_education = models.ManyToManyField(Education, related_name='resume_education')
    selected_experience = models.ManyToManyField(Experiences, related_name='resume_experience')
    selected_projects = models.ManyToManyField(Projects, related_name='resume_projects')

    areas_of_interest = models.CharField(max_length=255, null=True, blank=True)
    academic_qualification = models.TextField(null=True, blank=True)
    achievements = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(auto_now=True)

class JobListings(models.Model):
    job_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    job_url = models.URLField()
    requirements = models.ManyToManyField(Skills, blank=True)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListings, on_delete=models.CASCADE)
    application_id = models.AutoField(primary_key=True)
    applied_on = models.DateField(null=True, blank=True)
    next_follow_up_date = models.DateField(null=True, blank=True)
    application_medium = models.CharField(max_length=100, null=True, blank=True)
    application_status = models.CharField(max_length=100, null=True, blank=True)
    user_notes = models.TextField(null=True, blank=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s application for {self.job}"

class PublicDashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visibility_settings = models.JSONField(null=True, blank=True)
    profile_visibility = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    notification_type = models.CharField(
        max_length=100,
        choices=[
            ('job_update', 'Job Update'),
            ('profile_view', 'Profile View'),
            ('application_status', 'Application Status'),
            ('new_message', 'New Message'),
            ('system_alert', 'System Alert')
        ]
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.notification_type} - {self.user.username}"
