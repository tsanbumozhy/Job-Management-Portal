"""
URL configuration for jobnest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from jobnest_app.views import (
    home, logout_view,
    create_user, create_profile, profile_detail, continue_profile, edit_profile, create_additional_info, edit_additional_info, my_dashboard, add_education, add_experience,
    add_skill, add_skill_ajax,
    create_project, edit_project, delete_project, my_projects, project_detail, like_project, 
    create_resume_template, create_resume, preview_resume, generate_resume, edit_resume, resume_preview, delete_resume,
    create_job_listing_and_application, edit_job_application, all_job_listings, delete_job, my_progress, add_job_progress, progress_detail,
    search,
    mark_notification_as_read,
    UserViewSet, ProfileViewSet, ProjectsViewSet
)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)
router.register('projects', ProjectsViewSet)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('', home, name='home'),

    path('search/', search, name='search'),

    #path('project/<int:project_id>/pdf/', view_pdf, name='view_pdf'),
    
    path('user/', create_user, name='create_user'),
    path('profile/', create_profile, name='create_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/dashboard', my_dashboard, name='my_dashboard'),
    path('profile/additional/', create_additional_info, name='create_additional_info'),
    path('profile/additional/continue/', continue_profile, name='continue_profile'),
    path('profile/additional/edit/', edit_additional_info, name='edit_additional_info'),
    path('profile/additional/add_education/', add_education, name='add_education'),
    path('profile/additional/add_experience/', add_experience, name='add_experience'),
    path('profile/<str:username>/', profile_detail, name='profile_detail'),

    path('add_skill/', add_skill, name='add_skill'),
    path('add-skill-ajax/', add_skill_ajax, name='add_skill_ajax'),


    path('create_project/', create_project, name='create_project'),  

    path('project/my_projects/', my_projects, name='my_projects'),
    path('project/<str:project_id>/', project_detail, name='project_detail'),

    path('edit_project/<str:project_id>/', edit_project, name='edit_project'),
    path('delete_project/<str:project_id>/', delete_project, name='delete_project'),  
    path('project/<int:project_id>/like/', like_project, name='like_project'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    # Job Listing and Application Management
    path('job/create/', create_job_listing_and_application, name='create_job_listing_and_application'),
    path('job/edit/<int:application_id>/', edit_job_application, name='edit_job_application'),
    path('job/delete/<int:job_id>/', delete_job, name='delete_job'),
    path('job/listings/', all_job_listings, name='all_job_listings'),

    # User Progress
    path('progress/', my_progress, name='my_progress'),
    path('progress/<int:application_id>/', progress_detail, name='progress_detail'),
    path('add-job/', add_job_progress, name='add_job_progress'),

    # Resume Template Management
    path('resume-template/create/', create_resume_template, name='create_resume_template'),
    
    # Resume Creation & Management
    path('resume/generate/', generate_resume, name='generate_resume'),
    path('resume/create/', create_resume, name='create_resume'),
    path('resume/preview/<int:resume_id>/', preview_resume, name='preview_resume'),
    path('resume/edit/<int:resume_id>/', edit_resume, name='edit_resume'),
    path('resume/preview/<int:resume_id>/', resume_preview, name='resume_preview'),
    path('resume/delete/<int:resume_id>/', delete_resume, name='delete_resume'),


    path('notifications/mark_read/<int:notif_id>/', mark_notification_as_read, name='mark_notification_as_read')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)