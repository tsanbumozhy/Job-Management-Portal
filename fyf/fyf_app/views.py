from django.conf import settings
from rest_framework import viewsets
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill, Projects
from .serializers.serializers import UserSerializer, ProfileSerializer, SkillSerializer, ProjectsSerializer
from .forms import RegistrationForm, ProfileForm, SkillForm, ProjectForm
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def home(request):
    if request.user.is_authenticated:
        # User is logged in
        try:
            profile_details = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect('create_profile')
        projects = Projects.objects.all()
        skills = Skill.objects.all()
        return render(request, 'home.html', {
            'User': request.user,
            'Profile': profile_details,
            'Skills': skills,
            'Projects': projects
        })
    else:
        # User is not logged in
        return render(request, 'home.html')

def create_user(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            return redirect('create_profile')  # Redirect to profile creation page
    else:
        form = RegistrationForm()

    return render(request, 'profile/create_user.html', {'form': form})

@login_required
def create_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            projects = Projects.objects.all()
            skills = Skill.objects.all()
            return render(request, 'home.html', {
                'User': request.user,
                'Profile': request.user.profile,
                'Skills': skills,
                'Projects': projects
            })
    else:
        form = ProfileForm()

    return render(request, 'profile/create_profile.html', {'form': form})

@login_required
def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('create_profile')

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        user = request.user
        profile = ProfileForm(instance=profile)

    return render(request, 'profile/edit_profile.html', {'User': user, 'Profile': profile})
    
def search(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    projects = Projects.objects.all()
    skills = Skill.objects.all()
    
    query = request.GET.get('q')
    results = Projects.objects.filter(Q(title_icontains=query) | Q(description_icontains=query))

    return render(request, 'search_results.html', {'results': results, 'query': query, 'User': user_details, 'Profile': profile_details, 'Skills': skills})
    
def logout_view(request):
    logout(request)
    return redirect('home')
    
def skills(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all
    return render(request, 'skills.html', {'User': user_details, 'Profile': profile_details, 'Skills': skills})

def skill_projects(request, skill_name):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all

    skill = get_object_or_404(Skill, name=skill_name)
    projects = Projects.objects.filter(skill_id=skill.skill_id).order_by('title')
    return render(request, 'skill_projects.html', { 'User': user_details, 'Profile': profile_details, 'Skills': skills, 'Skill': skill, 'Projects': projects })

def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_project')
    else:
        form = SkillForm()
    
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all

    return render(request, 'write.html', {'form': form, 'User': user_details, 'Profile': profile_details, 'Skills': skills})

def project_details(request, project_id):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all 

    context = { 'User': user_details, 'Profile': profile_details, 'Skills': skills }

    return render(request, 'project_details.html', context)

def view_pdf(request, project_id):
    try:
        project = Projects.objects.get(project_id=project_id)
    except Projects.DoesNotExist:
        return render(request, 'error.html', {'message': 'project not found'})

    pdf_file_path = project.content_url.path
    response = FileResponse(open(pdf_file_path, 'rb'), content_type='application/pdf')
    return response

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            return redirect('home')
    else:
        form = ProjectForm()

    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all

    return render(request, 'write.html', {'form': form, 'User': user_details, 'Profile': profile_details, 'Skills': skills})

def my_projects(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all

    projects = Projects.objects.filter(author=user_details.id).order_by('title')

    context = { 'User': user_details, 'Profile': profile_details, 'Skills': skills, 'Projects':projects, 'Flag':1 }

    return render(request, 'profile/profile_pages.html', context)

class LoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        username = self.request.user.username
        print(username)
        return reverse_lazy('home') + '?username=' + username

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer

    def perform_create(self, serializer):
        uploaded_file = self.request.FILES.get('content_url')
        if uploaded_file:
            serializer.save(content_url=uploaded_file)
        else:
            serializer.save()
        
        uploaded_file = self.request.FILES.get('cover_image')
        if uploaded_file:
            serializer.save(cover_image=uploaded_file)
        else:
            serializer.save()
