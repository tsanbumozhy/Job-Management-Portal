from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
    
class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    bio = models.TextField()
    github_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
    portfolio_url = models.URLField(max_length=255, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.profile_id)

class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)
    
class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tech_stack = models.JSONField(null=True, blank=True)
    skills = models.ManyToManyField(Skill, related_name='projects')
    live_url = models.URLField(max_length=255, null=True, blank=True)
    github_repo_url = models.URLField(max_length=255, null=True, blank=True)
    cover_image = models.ImageField(upload_to='project_covers/', null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.project_id)

class JobListing(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    job_url = models.URLField(max_length=255)
    requirements = models.TextField()
    tech_stack = models.JSONField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    job_type = models.CharField(max_length=100, choices=[('full-time', 'Full-Time'), ('part-time', 'Part-Time'), ('internship', 'Internship'), ('contract', 'Contract')])

    created_at = models.DateTimeField(default=timezone.now)

class JobApplication(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    applied_on = models.DateTimeField()
    next_follow_up_date = models.DateTimeField(null=True, blank=True)
    application_medium = models.CharField(max_length=100, null=True, blank=True)
    application_status = models.CharField(max_length=100, choices=[('applied', 'Applied'), ('interview', 'Interview'), ('rejected', 'Rejected'), ('offer', 'Offer'), ('withdrawn', 'Withdrawn'), ('ghosted', 'Ghosted') ])
    user_notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)

    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    template_file = models.FileField(upload_to='resume_templates/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(auto_now=True)

class PublicDashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visibility_settings = models.JSONField(null=True, blank=True)
    profile_visibility = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=100, choices=[('job_update', 'Job Update'), ('profile_view', 'Profile View'), ('application_status', 'Application Status'), ('new_message', 'New Message'), ('system_alert', 'System Alert')])

    created_at = models.DateTimeField(default=timezone.now)
