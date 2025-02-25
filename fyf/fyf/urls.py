"""
URL configuration for fyf project.

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
from fyf_app.views import UserViewSet, ProfileViewSet, SkillViewSet, ProjectsViewSet, LikeViewSet, CommentViewSet
from fyf_app.views import home, search, logout_view, skills, skill_projects, create_user, create_project, project_details, edit_profile, like
from fyf_app.views import my_projects, read_list, favourites, add_skill, add_comment, edit_comment, delete_comment, view_pdf

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)
router.register('skills', SkillViewSet)
router.register('projects', ProjectsViewSet)
router.register('likes', LikeViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('', home, name='home'),

    path('search/', search, name='search'),

    path('add_skill/', add_skill, name='add_skill'),

    path('create_project/', create_project, name='create_project'),
    path('project/<str:project_id>/', project_details, name='project_details'),

    path('project/<int:project_id>/pdf/', view_pdf, name='view_pdf'),

    path('project/<str:project_id>/like', like, name='add_like'),
    path('project/<int:project_id>/add_comment/', add_comment, name='add_comment'),
    
    path('project/<int:project_id>/edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('project/<int:project_id>/delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),

    path('skills/', skills, name='skills'),
    path('skill_projects/<str:skill_name>/', skill_projects, name='skill_projects'),
    
    path('create_user/', create_user, name='create_user'),

    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/my_list/', my_projects, name='my_list'),
    path('profile/read_list/', read_list, name='read_list'),
    path('profile/favourites/', favourites, name='liked_projects'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)