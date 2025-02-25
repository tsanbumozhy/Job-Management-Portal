from django.conf import settings
from rest_framework import viewsets
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill, Projects, Like, Comment
from .serializers.serializers import UserSerializer, ProfileSerializer, SkillSerializer, ProjectsSerializer, LikeSerializer, CommentSerializer
from .forms import RegistrationForm, ProfileForm, SkillForm, ProjectForm, CommentForm

from django.shortcuts import render, redirect, get_object_or_404

@login_required
def home(request):
    if request.user.is_authenticated:
        # User is logged in
        username = request.user.username
        user_details = User.objects.get(username=username)
        profile_details = Profile.objects.get(user=user_details.id)
        projects = Projects.objects.all()
        skills = Skill.objects.all()
        return render(request, 'home.html', {'User': user_details, 'Profile': profile_details, 'Skills': skills, 'Projects': projects})
    else:
        # User is not logged in
        return render(request, 'home.html')
    
def search(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    projects = Projects.objects.all()
    skills = Skill.objects.all()
    
    query = request.GET.get('q')
    results = Projects.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

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

def create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            profile = Profile(
                user=user,
                pen_name=form.cleaned_data['pen_name'],
                bio=form.cleaned_data['bio'],
                profile_photo=request.FILES.get('profile_photo')
            )
            profile.save()

            projects = Projects.objects.all()
            skills = Skill.objects.all()
            return render(request, 'home.html', {'User': user, 'Profile': profile, 'Skills': skills, 'Projects': projects})
    else:
        form = RegistrationForm()
    
    return render(request, 'profile/create_user.html', {'form': form})

def project_details(request, project_id):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all

    project = get_object_or_404(Projects, project_id=project_id)

    read = Like.objects.filter(profile=profile_details, project=project)
    if not read:
        Like.objects.create(profile=profile_details, project=project, liked=False)

    like_status = Like.objects.get(profile=profile_details, project=project)

    comments = Comment.objects.filter(project=project)

    read_count = Like.objects.filter(project=project).count()
    likes_count = Like.objects.filter(project=project, liked=True).count()
    comment_count = Comment.objects.filter(project=project).count() 

    count = { 'reads': read_count, 'likes': likes_count, 'num_comment': comment_count }

    context = { 'User': user_details, 'Profile': profile_details, 'Skills': skills, 'Project': project, 'Like': like_status, 'Comments': comments, 'Count': count }

    return render(request, 'project_details.html', context)

def view_pdf(request, project_id):
    try:
        project = Projects.objects.get(project_id=project_id)
    except Projects.DoesNotExist:
        return render(request, 'error.html', {'message': 'project not found'})

    pdf_file_path = project.content_url.path

    response = FileResponse(open(pdf_file_path, 'rb'), content_type='application/pdf')
    return response

def like(request, project_id):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all

    project = get_object_or_404(Projects, project_id=project_id)

    like_status = Like.objects.get(profile=profile_details, project=project)

    like_status.liked = not like_status.liked
    like_status.save()

    comments = Comment.objects.filter(project=project)

    read_count = Like.objects.filter(project=project).count()
    likes_count = Like.objects.filter(project=project, liked=True).count()
    comment_count = Comment.objects.filter(project=project).count() 

    count = { 'reads': read_count, 'likes': likes_count, 'num_comment': comment_count }

    context = { 'User': user_details, 'Profile': profile_details, 'Skills': skills, 'Project': project, 'Like': like_status, 'Comments': comments, 'Count': count }

    return render(request, 'project_details.html', context)

def add_comment(request, project_id):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all

    project = get_object_or_404(Projects, project_id=project_id)

    if request.method == 'POST':
        comment_text = request.POST['comment']

        comment = Comment(profile=profile_details, project=project, comment=comment_text)
        comment.save()    

    read = Like.objects.filter(profile=profile_details, project=project)
    if not read:
        Like.objects.create(profile=profile_details, project=project, liked=False)

    like_status = Like.objects.get(profile=profile_details, project=project)

    comments = Comment.objects.filter(project=project)

    read_count = Like.objects.filter(project=project).count()
    likes_count = Like.objects.filter(project=project, liked=True).count()
    comment_count = Comment.objects.filter(project=project).count() 

    count = { 'reads': read_count, 'likes': likes_count, 'num_comment': comment_count }

    context = { 'User': user_details, 'Profile': profile_details, 'Skills': skills, 'Project': project, 'Like': like_status, 'Comments': comments, 'Count': count }

    return render(request, 'project_details.html', context)

def edit_comment(request, project_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        updated_comment_text = request.POST['comment']

        if comment.profile.user == request.user:
            comment.comment = updated_comment_text
            comment.last_updated = timezone.now()
            comment.save()

            messages.success(request, 'Comment updated successfully.')
        else:
            messages.error(request, 'You are not authorized to edit this comment.')

        return redirect('project_details', project_id=comment.project.project_id)

    return redirect('project_details', project_id=comment.project.project_id)

def delete_comment(request, project_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        if comment.profile.user == request.user:
            comment.delete()

            messages.success(request, 'Comment deleted successfully.')
        else:
            messages.error(request, 'You are not authorized to delete this comment.')

        return redirect('project_details', project_id=comment.project.project_id)

    
    return redirect('project_details', project_id=comment.project.project_id)
    
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

def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)

    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all
    
    return render(request, 'profile/edit_profile.html', {'form': form, 'User': user_details, 'Profile': profile_details, 'Skills': skills})

def my_projects(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all

    projects = Projects.objects.filter(author=user_details.id).order_by('title')

    context = { 'User': user_details, 'Profile': profile_details, 'Skills': skills, 'Projects':projects, 'Flag':1 }

    return render(request, 'profile/profile_pages.html', context)

def read_list(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all
    projects = Projects.objects.all

    liked_projects = Projects.objects.filter(like__profile=profile_details)

    context = { 'User': user_details, 'Profile': profile_details, 'Skills': skills, 'Projects':liked_projects, 'Flag':2 }

    return render(request, 'profile/profile_pages.html', context)

def favourites(request):
    username = request.user.username
    user_details = User.objects.get(username=username)
    profile_details = Profile.objects.get(user=user_details.id)
    skills = Skill.objects.all
    projects = Projects.objects.all

    liked_projects = Projects.objects.filter(like__profile=profile_details, like__liked=True)

    context = { 'User': user_details, 'Profile': profile_details, 'Skills': skills, 'Projects':liked_projects, 'Flag':3 }

    return render(request, 'profile/profile_pages.html', context)

    project = Project.objects.get(id=project_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            return redirect('project_details', project_id=project_id)
    else:
        form = CommentForm()
    
    return render(request, 'add_comment.html', {'form': form, 'project': project})

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

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
