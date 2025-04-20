from rest_framework import serializers
from django.contrib.auth.models import User
from jobnest_app.models import Profile, AdditionalInfo, Skills, Projects, Education, Experiences, JobListings, ResumeTemplates, Resumes, JobApplications, PublicDashboard, Notifications

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'profile_id', 'full_name', 'objective', 'profile_photo']

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = [
            'user',
            'gender',
            'date_of_birth',
            'languages_known',
            'mobile_number',
            'address',
            'location',
            'github_url',
            'linkedin_url',
            'portfolio_url',
            'skills',
            'achievements',
            'resume_file'
        ]

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class ExperiencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiences
        fields = '__all__'

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['project_id', 'author', 'title', 'description', 'tech_stack', 'skills', 'live_url', 'github_repo_url', 'cover_image', 'created_at', 'updated_at']

class JobListingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListings
        fields = '__all__'

class ResumeTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeTemplates
        fields = ['id', 'name', 'html_file', 'css_file', 'preview_image', 'created_at']

class ResumesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resumes
        fields = [
            'user',
            'template',
            'full_name',
            'objective',
            'profile_photo',
            'languages_known',
            'mobile_number',
            'address',
            'location',
            'github_url',
            'linkedin_url',
            'portfolio_url',
            'skills',
            'selected_education',
            'selected_experience',
            'selected_projects',
            'achievements',
            'areas_of_interest',
            'created_at',
            'updated_at'
        ]

class JobApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplications
        fields = '__all__'

class PublicDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicDashboard
        fields = '__all__'

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'
