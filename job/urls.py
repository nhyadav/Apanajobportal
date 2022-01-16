from django.urls import path
from . import views

urlpatterns = [
    path('jobs', views.jobs, name='jobs'),
    path('profile', views.profile, name='profile'),
    path('profile/edit/<int:id>', views.edit_profile, name="edit_profile"),
    path('job/create', views.job_create, name='new_job'),
    path('job/edit/<int:id>', views.job_edit, name='editjob'),
    path('job/view/<int:id>', views.job_view, name='viewjob'),
    path('job/delete/<int:id>', views.deletejob, name="deletejob"),
    path("job/publish/<int:id>", views.publishjob, name="publishjob"),
    path("job/apply/<int:jobid>", views.applyjob, name="applyjob"),
    path("job/save/<int:jobid>", views.savejob, name="savejob")


]
