from django.contrib import admin
from fyf_app.models import Profile, Skill, Projects, Like, Comment

# Register your models here.

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Projects)
admin.site.register(Like)
admin.site.register(Comment)

