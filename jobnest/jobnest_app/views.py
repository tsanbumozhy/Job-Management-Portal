from django.conf import settings
from rest_framework import viewsets
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.forms import modelform_factory, modelformset_factory
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, FileResponse
from django.template import Template, Context
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, AdditionalInfo, Skills, Projects, Education, Experiences, Resumes, ResumeTemplates, JobListings, JobApplications, Notifications
from .serializers.serializers import UserSerializer, ProfileSerializer, AdditionalInfoSerializer, SkillsSerializer, ProjectsSerializer
from .forms import RegistrationForm, ProfileForm, AdditionalInfoForm, SkillForm, ProjectForm, EducationForm, ExperienceForm, ResumeTemplateForm, ResumeForm, JobListingForm, JobApplicationForm
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def home(request):
    try:
        profile_details = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('create_profile')

    all_projects = Projects.objects.all().select_related('author')
    today = timezone.now()
    recent_threshold = today - timedelta(days=7)

    my_projects = all_projects.filter(author=request.user)[:5]
    current_projects = all_projects.exclude(author=request.user).filter(created_at__gte=recent_threshold)[:3]
    active_projects = all_projects.exclude(author=request.user).order_by('-views', '-likes')[:5]

    notif_list = Notifications.objects.filter(user=request.user, is_read=False).order_by('-created_at')

    return render(request, 'home.html', {
        'User': request.user,
        'Profile': profile_details,
        'MyProjects': my_projects,
        'CurrentProjects': current_projects,
        'ActiveProjects': active_projects,
        'NotifList': notif_list,
        'NotifCount': notif_list.count(),
    })

    
def logout_view(request):
    logout(request)
    return redirect('home')

def create_user(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_profile')
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
            return render(request, 'home.html', {
                'User': request.user,
                'Profile': request.user.profile,
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

    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save(user=user)
            return redirect('home')
    else:
        profile = ProfileForm(instance=profile)

    return render(request, 'profile/edit_profile.html', {'User': user, 'Profile': profile})

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    additional_info = get_object_or_404(AdditionalInfo, user=user)

    all_projects = Projects.objects.all().select_related('author')
    all_users = User.objects.all().select_related('username')

    projects = all_projects.filter(author=user).order_by('-created_at')
    users = all_users.filter(username=user)

    return render(request, 'profile/profile_detail.html', {
        'additional_info': additional_info,
        'profile': profile,
        'user': user,
        'Projects': projects
    })

@login_required
def create_additional_info(request):
    try:
        additional_info = AdditionalInfo.objects.get(user=request.user)
    except AdditionalInfo.DoesNotExist:
        additional_info = None

    if request.method == 'POST':
        form = AdditionalInfoForm(request.POST, user=request.user)
        if form.is_valid():
            additional_info_obj = form.save(commit=False)
            additional_info_obj.user = request.user
            additional_info_obj.save()
            return redirect('continue_profile')
    else:
        form = AdditionalInfoForm(instance=additional_info)

    return render(request, 'profile/create_dashboard.html', {'form': form})

@login_required
def continue_profile(request):
    educations = Education.objects.filter(user=request.user)
    experiences = Experiences.objects.filter(user=request.user)

    return render(request, 'profile/profile_continue.html', {
        'educations': educations,
        'experiences': experiences,
    })


@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return redirect('continue_profile')
    else:
        form = EducationForm()

    return render(request, 'profile/add_education.html', {'form': form})

@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return redirect('continue_profile')
    else:
        form = ExperienceForm()

    return render(request, 'profile/add_experience.html', {'form': form})

@login_required
def edit_additional_info(request):
    try:
        profile = Profile.objects.get(user=request.user)
        additional_info = AdditionalInfo.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('create_profile')
    except AdditionalInfo.DoesNotExist:
        return redirect('create_additional_info')

    if request.method == "POST":
        form = AdditionalInfoForm(request.POST, request.FILES, instance=additional_info)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AdditionalInfoForm(instance=additional_info)

    return render(request, 'profile/complete_additional_info.html', {'User': request.user, 'Profile': profile, 'AdditionalInfo': additional_info})

@login_required
def my_dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    try:
        profile = Profile.objects.get(user=request.user)
        additional_info = AdditionalInfo.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('create_profile')
    except AdditionalInfo.DoesNotExist:
        return redirect('create_additional_info')
    
    all_projects = Projects.objects.all().select_related('author')

    my_projects = all_projects.filter(author=request.user).order_by('-created_at')

    educations = Education.objects.filter(user=request.user)
    experiences = Experiences.objects.filter(user=request.user)

    return render(request, 'profile/my_dashboard.html', {
        'user': request.user,
        'profile': profile,
        'additional_info': additional_info,
        'educations': educations,
        'experiences': experiences,
        'MyProjects': my_projects })

@login_required
def my_projects(request):
    all_projects = Projects.objects.all().select_related('author')

    my_projects = all_projects.filter(author=request.user).order_by('-created_at')

    return render(request, 'projects/my_projects.html', {
        'User': request.user,
        'Profile': request.user.profile,
        'MyProjects': my_projects
    })

@csrf_exempt
def add_skill_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')

        if not name:
            return JsonResponse({'error': 'Missing name'}, status=400)
        if not category:
            return JsonResponse({'error': 'Missing category'}, status=400)

        skill, created = Skills.objects.get_or_create(
            name=name,
            defaults={'category': category}
        )

        return JsonResponse({
            'id': skill.skill_id,
            'name': skill.name,
            'category': skill.category,
            'created': created
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_skill(request):
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user  # Assuming Skills model has a user field
            skill.save()
            return redirect('home')
    else:
        form = SkillForm()

    return render(request, 'add_skill.html', {'form': form})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('my_projects')
    else:
        form = ProjectForm()

    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def edit_project(request, pk):
    try:
        project = Projects.objects.get(pk=pk, author=request.user)
    except Projects.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('home')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Projects, project_id=project_id, author=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('home')
    return render(request, 'projects/delete_confirm.html', {'project': project})

def project_detail(request, project_id):
    project = get_object_or_404(Projects, project_id=project_id)

    project.views += 1
    project.save(update_fields=['views'])

    return render(request, 'projects/project_detail.html', {
        'project': project
    })

@csrf_exempt  # or use `@login_required` + CSRF token if needed
def like_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Projects, project_id=project_id)
        project.likes += 1
        project.save(update_fields=['likes'])
        return JsonResponse({'likes': project.likes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def create_resume_template(request):
    if request.method == "POST":
        form = ResumeTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ResumeTemplateForm()

    return render(request, 'resume/create_resume_template.html', {'form': form})

@login_required
def generate_resume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            form.save()  # Save many-to-many relationships
            return redirect('home')  # Or redirect to resume preview
    else:
        form = ResumeForm(user=request.user)

    return render(request, 'resume/edit_resume.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def edit_resume(request, resume_id):
    try:
        resume = Resumes.objects.get(id=resume_id, user=request.user)
    except Resumes.DoesNotExist:
        return redirect('home')

    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, instance=resume, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')  # Or to resume preview
    else:
        form = ResumeForm(instance=resume, user=request.user)

    return render(request, 'resume/edit_resume.html', {
        'form': form,
        'resume': resume,
        'action': 'Edit'
    })

@login_required
def resume_preview(request, resume_id):
    resume = get_object_or_404(Resumes, id=resume_id, user=request.user)
    return render(request, 'resume/preview.html', {'resume': resume})

@login_required
def create_resume(request):
    templates = ResumeTemplates.objects.all()
    user = request.user
    educations = Education.objects.filter(user=user)
    experiences = Experiences.objects.filter(user=user)
    profile = get_object_or_404(Profile, user=user)
    additional_info = get_object_or_404(AdditionalInfo, user=user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        selected_template_id = request.POST.get('template_id')

        if form.is_valid() and selected_template_id:
            resume = form.save(commit=False)
            resume.template = get_object_or_404(ResumeTemplates, id=selected_template_id)
            resume.user = request.user
            resume.save()
            form.save_m2m()
            return redirect('preview_resume', resume_id=resume.resume_id)
    else:
        form = ResumeForm()

    return render(request, 'resume/create_resume.html', {
        'form': form,
        'templates': templates,
        'user': user,
        'profile': profile,
        'additional_info': additional_info,
        'educations': educations,
        'experiences': experiences
    })

@login_required
def preview_resume(request, resume_id):
    resume = get_object_or_404(Resumes, resume_id=resume_id)
    template_file = resume.template.html_file.path
    css_file = resume.template.css_file.url
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    additional_info = get_object_or_404(AdditionalInfo, user=user)

    with open(template_file, 'r', encoding='utf-8') as file:
        html_template = Template(file.read())

    context = Context({
        **resume.__dict__,
        'skills': resume.skills.all(),
        'selected_education': resume.selected_education.all(),
        'selected_experience': resume.selected_experience.all(),
        'selected_projects': resume.selected_projects.all(),
        'css_file': css_file,
        'user': user,
        'profile': profile,
        'additional_info': additional_info,
        'areas_of_interest_list': resume.areas_of_interest.split(',') if resume.areas_of_interest else [],
        'achievements_list': resume.achievements.split('\n') if resume.achievements else [],
    })

    rendered_html = html_template.render(context)
    return HttpResponse(rendered_html)

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resumes, id=resume_id, user=request.user)
    if request.method == 'POST':
        resume.delete()
        return redirect('home')
    return render(request, 'resume/delete_confirm.html', {'resume': resume})

@login_required
def create_job_listing_and_application(request):
    if request.method == "POST":
        job_form = JobListingForm(request.POST)
        application_form = JobApplicationForm(request.POST, request.FILES)

        if job_form.is_valid() and application_form.is_valid():
            job = job_form.save()
            application = application_form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            return redirect('home')
    else:
        job_form = JobListingForm()
        application_form = JobApplicationForm()

    return render(request, 'job/my_progress.html', {
        'job_form': job_form,
        'app_form': application_form
    })

@login_required
def edit_job_application(request, application_id):
    try:
        application = JobApplications.objects.get(id=application_id, user=request.user)
    except JobApplications.DoesNotExist:
        return redirect('home')

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = JobApplicationForm(instance=application)

    return render(request, 'job/my_progress.html', {
        'form': form,
        'application': application
    })

# Job Listing Views
def all_job_listings(request):
    jobs = JobListings.objects.all().order_by('-created_at')
    return render(request, 'job/my_progress.html', {'jobs': jobs})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobListings, id=job_id)

    # Optional: Only allow deletion by creator or admin
    if request.user != job.created_by and not request.user.is_staff:
        return redirect('job_detail', job_id=job.id)  # or show permission denied

    if request.method == 'POST':
        job.delete()
        return redirect('job_listings')  # Redirect to job listings page

    return render(request, 'jobs/delete_confirm.html', {'job': job})

@login_required
def my_progress(request):
    job_applications = JobApplications.objects.filter(user=request.user).select_related('job')

    return render(request, 'job/my_progress.html', {
        'job_applications': job_applications
    })

@login_required
def add_job_progress(request):
    if request.method == 'POST':
        job_form = JobListingForm(request.POST)
        app_form = JobApplicationForm(request.POST, request.FILES)

        if job_form.is_valid() and app_form.is_valid():
            job = job_form.save()

            app = app_form.save(commit=False)
            app.user = request.user
            app.job = job
            app.save()
            app_form.save_m2m()

            return redirect('my_progress')
    else:
        job_form = JobListingForm()
        app_form = JobApplicationForm()

    return render(request, 'job/create_job.html', {
        'job_form': job_form,
        'app_form': app_form
    })

@login_required
def progress_detail(request, application_id):
    application = get_object_or_404(JobApplications, application_id=application_id)
    return render(request, 'job/progress_detail.html', {
        'application': application,
        'job': application.job
    })

@login_required
def search(request):
    user = request.user
    query = request.GET.get('q', '').strip()

    profile_details = getattr(user, 'profile', None)

    project_results = Projects.objects.filter(
        Q(title__icontains=query) |
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(skills__name__icontains=query)
    ).distinct()

    profile_results = Profile.objects.filter(
        Q(user__username__icontains=query) |
        Q(full_name__icontains=query)
    ).distinct()

    return render(request, 'search_results.html', {
        'projects': project_results,
        'profiles': profile_results,
        'query': query,
        'User': user,
        'Profile': profile_details
    })

@login_required
def project_details(request, project_id):
    user = request.user
    profile = Profile.objects.get(user=user)

    projects = get_object_or_404(Projects, project_id=project_id)

    return render(request, 'profile/profile_view.html', {
        'user': user,
        'profile': profile,
        'projects': projects })

@csrf_exempt
def mark_notification_as_read(request, notif_id):
    if request.method == 'POST':
        notif = Notifications.objects.filter(id=notif_id, user=request.user).first()
        if notif:
            notif.is_read = True
            notif.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

# DRF ViewSets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
