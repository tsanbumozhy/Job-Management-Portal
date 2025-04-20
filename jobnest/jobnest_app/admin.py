from django.contrib import admin
from jobnest_app.models import (
    Profile,
    AdditionalInfo,
    Skills,
    Projects,
    Education,
    Experiences,
    ResumeTemplates,
    Resumes,
    JobListings,
    JobApplications,
)

# Register your models here
admin.site.register(Profile)
admin.site.register(AdditionalInfo)
admin.site.register(Skills)
admin.site.register(Projects)
admin.site.register(Education)
admin.site.register(Experiences)
admin.site.register(ResumeTemplates)
admin.site.register(Resumes)
admin.site.register(JobListings)
admin.site.register(JobApplications)
