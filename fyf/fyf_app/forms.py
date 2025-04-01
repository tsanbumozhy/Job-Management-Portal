from django import forms
from django.core.files import File
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Projects, Skill, Education, Experience, JobListing, JobApplication

INDIAN_CITIES = [
    ('Mumbai', 'Mumbai'), ('Delhi', 'Delhi'), ('Bangalore', 'Bangalore'), 
    ('Hyderabad', 'Hyderabad'), ('Chennai', 'Chennai'), ('Kolkata', 'Kolkata'),
    ('Pune', 'Pune'), ('Jaipur', 'Jaipur'), ('Ahmedabad', 'Ahmedabad'),
    ('Lucknow', 'Lucknow'), ('Surat', 'Surat'), ('Chandigarh', 'Chandigarh'),
    ('Bhopal', 'Bhopal'), ('Indore', 'Indore'), ('Patna', 'Patna'),
    ('Nagpur', 'Nagpur'), ('Coimbatore', 'Coimbatore'), ('Mysore', 'Mysore'),
    ('Others', 'Others')
]

APPLICATION_MEDIUM_CHOICES = [
    ('LinkedIn', 'LinkedIn'),
    ('On-Campus', 'On-Campus'),
    ('Off-Campus', 'Off-Campus'),
    ('Others', 'Others')
]

APPLICATION_STATUS_CHOICES = [
    ('Applied', 'Applied'),
    ('Interview', 'Interview'),
    ('Rejected', 'Rejected'),
    ('Offer', 'Offer'),
    ('Withdrawn', 'Withdrawn'),
    ('Ghosted', 'Ghosted')
]

JOB_TYPE_CHOICES = [
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time'),
    ('Internship', 'Internship'),
    ('Contract', 'Contract')
]

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 35, 'placeholder': 'Short bio'}), required=False)
    github_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'GitHub profile URL'}), required=False)
    linkedin_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'LinkedIn profile URL'}), required=False)
    portfolio_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Portfolio website URL'}), required=False)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'github_url', 'linkedin_url', 'portfolio_url', 'profile_photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'cols': 35, 'placeholder': 'Short bio'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'GitHub profile URL'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'LinkedIn profile URL'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'Portfolio website URL'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'my-custom-class'})
        }

    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')
        if github_url and not github_url.startswith("https://github.com/"):
            raise forms.ValidationError("Enter a valid GitHub profile URL.")
        return github_url

    def clean_linkedin_url(self):
        linkedin_url = self.cleaned_data.get('linkedin_url')
        if linkedin_url and not linkedin_url.startswith("https://linkedin.com/"):
            raise forms.ValidationError("Enter a valid LinkedIn profile URL.")
        return linkedin_url

    def save(self, user):
        profile = Profile.objects.create(user=user)
        profile.user = user
        profile.full_name = self.cleaned_data['full_name']
        profile.bio = self.cleaned_data['bio']
        profile.github_url = self.cleaned_data['github_url']
        profile.linkedin_url = self.cleaned_data['linkedin_url']
        profile.portfolio_url = self.cleaned_data['portfolio_url']
        
        profile_photo = self.cleaned_data.get('profile_photo')
        if profile_photo:
            profile.profile_photo.save(profile_photo.name, File(profile_photo))
        
        profile.save()
        return profile

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']  # Only field needed in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill name'}),
        }
    
    def clean_name(self):
        """Ensure skill name is unique (case insensitive)."""
        name = self.cleaned_data.get('name')
        if Skill.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This skill already exists.")
        return name

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'description', 'tech_stack', 'skills', 'live_url', 'github_repo_url', 'cover_image']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter project description'}),
            'tech_stack': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter tech stack as JSON or comma-separated'}),
            'skills': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'live_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter live URL (if any)'}),
            'github_repo_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter GitHub repository URL'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_tech_stack(self):
        """Validate tech_stack input (convert comma-separated to JSON)."""
        tech_stack = self.cleaned_data.get('tech_stack')
        try:
            import json
            tech_stack_data = json.loads(tech_stack)  # Try to parse JSON
            if not isinstance(tech_stack_data, list):
                raise ValueError
            return tech_stack_data
        except (ValueError, TypeError):
            return [tech.strip() for tech in tech_stack.split(',') if tech.strip()]  # Convert comma-separated

    def save(self, commit=True, user=None):
        """Override save to assign the logged-in user as author."""
        project = super().save(commit=False)
        if user:
            project.author = user  # Assign logged-in user as author
        if commit:
            project.save()
            self.save_m2m()  # Save many-to-many relationships (skills)
        return project

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['title', 'institution', 'start_year', 'end_year', 'score']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter degree name'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter institution name'}),
            'start_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_year': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter score (if applicable)', 'step': '0.01', 'min': 0, 'max': 10}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['job_title', 'description', 'company_name', 'start_date', 'end_date']

        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter job description', 'rows': 3}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class JobListingForm(forms.ModelForm):
    requirements = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )

    location = forms.ChoiceField(
        choices=[('', 'Select City')] + INDIAN_CITIES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = JobListing
        fields = ['title', 'company', 'description', 'job_url', 'requirements', 'tech_stack', 'location', 'job_type']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter job description', 'rows': 4}),
            'job_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter job application link'}),
            'tech_stack': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter technologies (comma-separated)'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}, choices=[('full-time', 'Full-Time'), ('part-time', 'Part-Time'), ('internship', 'Internship'), ('contract', 'Contract')]),
        }


class JobApplicationForm(forms.ModelForm):
    job = forms.ModelChoiceField(
        queryset=JobListing.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    profile = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    applied_on = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    next_follow_up_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

    application_medium = forms.ChoiceField(
        choices=[('', 'Select Application Medium')] + APPLICATION_MEDIUM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    application_status = forms.ChoiceField(
        choices=[('', 'Select Status')] + APPLICATION_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    user_notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add any notes...'}),
        required=False
    )

    class Meta:
        model = JobApplication
        fields = ['job', 'profile', 'applied_on', 'next_follow_up_date', 'application_medium', 'application_status', 'user_notes']