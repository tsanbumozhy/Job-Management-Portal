from django import forms
from django.core.files import File
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from datetime import datetime

from .models import Profile, AdditionalInfo, Projects, Skills, Education, Experiences, ResumeTemplates, Resumes, JobListings, JobApplications 

PROJECT_CATEGORY = [
    ('industry', 'Industry Based Project Experience'), 
    ('non_academic', 'Non-Academic Projects'), 
    ('academic', 'Academic Projects')
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
    objective = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 35, 'placeholder': 'Short objective'}))

    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['full_name', 'objective', 'profile_photo']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'objective': forms.Textarea(attrs={'rows': 3, 'cols': 35, 'placeholder': 'Short objective'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'my-custom-class'})
        }

    def save(self, user):
        profile, created = Profile.objects.get_or_create(user=user)
        profile.user = user
        profile.full_name = self.cleaned_data['full_name']
        profile.objective = self.cleaned_data['objective']
        
        profile_photo = self.cleaned_data.get('profile_photo')
        if profile_photo:
            profile.profile_photo.save(profile_photo.name, File(profile_photo))
        
        profile.save()
        return profile
    
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill name'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter skill's category"})
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').strip()
        category = cleaned_data.get('category', '').strip()

        if Skills.objects.filter(name__iexact=name, category__iexact=category).exists():
            raise forms.ValidationError("This skill already exists.")

        cleaned_data['name'] = name
        cleaned_data['category'] = category
        return cleaned_data

class AdditionalInfoForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=[('Other', 'Other'), ('Male', 'Male'), ('Female', 'Female')], required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    languages_known = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'English, Tamil, Hindi'}))

    mobile_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your mobile number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your address', 'rows': 3}))
    location = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your location'}))

    github_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'GitHub profile URL'}), required=False)
    linkedin_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'LinkedIn profile URL'}), required=False)
    portfolio_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Portfolio website URL'}), required=False)

    skills = forms.ModelMultipleChoiceField(queryset=Skills.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select2'}), required=False)

    achievements = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Mention achievements or certifications.', 'rows': 3}), required=False)

    resume_file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'}), required=False)

    class Meta:
        model = AdditionalInfo
        exclude = ['user']
        fields = ['gender', 'date_of_birth', 'languages_known', 'mobile_number', 'address', 'location', 'github_url', 'linkedin_url', 'portfolio_url', 'skills', 'achievements', 'resume_file']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            from datetime import date
            today = date.today()
            if dob >= today:
                raise forms.ValidationError("Date of birth cannot be in the future.")
        return dob

    def clean_languages_known(self):
        languages = self.cleaned_data.get('languages_known')
        if languages:
            cleaned = [lang.strip() for lang in languages.split(',') if lang.strip()]
            return ', '.join(cleaned)
        return languages

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['title', 'institution', 'start_year', 'end_year', 'score']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter degree name'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter institution name'}),
            'start_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Start year',
                'min': '1900',
                'max': '2099',
                'step': '1'
            }),
            'end_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'End year',
                'min': '1900',
                'max': '2099',
                'step': '1'
            }),
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter score',
                'step': '0.01',
                'min': 0,
                'max': 100
            }),
        }

class ExperienceForm(forms.ModelForm):
    start_date = forms.CharField(widget=forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}))
    end_date = forms.CharField(required=False, widget=forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}))

    class Meta:
        model = Experiences
        fields = ['job_title', 'description', 'company_name', 'start_date', 'end_date']

    def clean_start_date(self):
        data = self.cleaned_data['start_date']
        return datetime.strptime(data, '%Y-%m').date()

    def clean_end_date(self):
        data = self.cleaned_data.get('end_date')
        if data:
            return datetime.strptime(data, '%Y-%m').date()
        return None

class ProjectForm(forms.ModelForm):
    category = forms.ChoiceField( choices = PROJECT_CATEGORY, widget=forms.Select(attrs={'class': 'form-control'}))

    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter a name for the project'}))
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter project title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter project description', 'rows': 3}), required=False)
    skills = forms.ModelMultipleChoiceField(queryset=Skills.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select2'}), required=False)
    github_repo_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'GitHub project URL'}), required=False)
    live_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Live project URL'}), required=False)

    cover_image = forms.ImageField(required=False)

    class Meta:
        model = Projects
        fields = ['name', 'title', 'description', 'skills', 'live_url', 'github_repo_url', 'cover_image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a name for the project'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter project description'}),
            'skills': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'live_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter live URL (if any)'}),
            'github_repo_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter GitHub repository URL'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True, user=None):
        project = super().save(commit=False)
        if user:
            project.author = user

        cover_image = self.cleaned_data.get('cover_image')
        if cover_image:
            project.cover_image.save(cover_image.name, File(cover_image))

        if commit:
            project.save()
            self.save_m2m()

        return project

    
class ResumeTemplateForm(forms.ModelForm):
    class Meta:
        model = ResumeTemplates
        fields = ['name', 'html_file', 'css_file', 'preview_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Template Name'}),
            'html_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'css_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'preview_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resumes
        fields = [
            'template', 'full_name', 'roll_number', 'objective', 'profile_photo',
            'languages_known', 'email', 'mobile_number', 'address', 'location',
            'github_url', 'linkedin_url', 'portfolio_url', 'skills',
            'selected_education', 'selected_experience', 'selected_projects',
            'areas_of_interest', 'academic_qualification', 'achievements'
        ]
        widgets = {
            'template': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'languages_known': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
            'skills': forms.SelectMultiple(attrs={'class': 'select2'}),
            'selected_education': forms.SelectMultiple(attrs={'class': 'select2'}),
            'selected_experience': forms.SelectMultiple(attrs={'class': 'select2'}),
            'selected_projects': forms.SelectMultiple(attrs={'class': 'select2'}),
            'areas_of_interest': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_qualification': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # ✅ Set required fields
        self.fields['objective'].required = True
        self.fields['skills'].required = True
        self.fields['selected_education'].required = True
        self.fields['selected_experience'].required = True
        self.fields['selected_projects'].required = True

        if user:
            self.fields['skills'].queryset = Skills.objects.filter(user=user)
            self.fields['selected_education'].queryset = Education.objects.filter(user=user)
            self.fields['selected_experience'].queryset = Experiences.objects.filter(user=user)
            self.fields['selected_projects'].queryset = Projects.objects.filter(user=user)

            if not self.instance.pk:
                profile = getattr(user, 'profile', None)
                additional = getattr(profile, 'additionalinfo', None)

                # ✅ Optional fields fallback to profile/additional
                if profile:
                    self.fields['full_name'].initial = profile.full_name
                    self.fields['roll_number'].initial = getattr(profile, 'roll_number', '')

                if additional:
                    self.fields['email'].initial = user.email
                    self.fields['mobile_number'].initial = additional.mobile_number
                    self.fields['address'].initial = additional.address
                    self.fields['location'].initial = additional.location
                    self.fields['github_url'].initial = additional.github_url
                    self.fields['linkedin_url'].initial = additional.linkedin_url
                    self.fields['portfolio_url'].initial = additional.portfolio_url
                    self.fields['profile_photo'].initial = additional.profile_photo
                    self.fields['languages_known'].initial = additional.languages_known
                    self.fields['objective'].initial = additional.objective
                    self.fields['areas_of_interest'].initial = additional.areas_of_interest
                    self.fields['academic_qualification'].initial = additional.academic_qualification
                    self.fields['achievements'].initial = additional.achievements

class JobListingForm(forms.ModelForm):
    requirements = forms.ModelMultipleChoiceField(queryset=Skills.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select2'}), required=False)

    class Meta:
        model = JobListings
        fields = ['title', 'company', 'description', 'job_url', 'requirements', 'location', 'job_type']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'requirements': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter job description', 'rows': 4}),
            'job_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter job application link'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}, choices=[('full-time', 'Full-Time'), ('part-time', 'Part-Time'), ('internship', 'Internship'), ('contract', 'Contract')]),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'})
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.title = instance.title.strip()

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class JobApplicationForm(forms.ModelForm):

    applied_on = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)
    next_follow_up_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)

    application_medium = forms.ChoiceField(choices=[('', 'Select Application Medium')] + APPLICATION_MEDIUM_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    application_status = forms.ChoiceField(choices=[('', 'Select Status')] + APPLICATION_STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    user_notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add any notes...'}), required=False)

    resume_file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'}), required=False)

    class Meta:
        model = JobApplications
        exclude = ['user', 'job']