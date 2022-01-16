from django.contrib import admin
from .models import Category, Job, Applicant, SaveJob, UserDetails, ApplyJob

admin.site.register(Category)
admin.site.register(ApplyJob)

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'timestamp')

admin.site.register(Applicant, ApplicationAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'is_closed', 'timestamp')

admin.site.register(Job,JobAdmin)

class SaveJobAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'timestamp')

admin.site.register(SaveJob, SaveJobAdmin)


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'contact_no', 'education')

admin.site.register(UserDetails, UserDetailsAdmin)
