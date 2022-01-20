from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#user details
class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    age = models.IntegerField()
    contact_no = models.CharField(max_length=12)
    education = models.CharField(max_length=50)
    address = models.TextField()
    country = models.CharField(max_length=50)
    company_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user.first_name + self.user.last_name
    





JOB_TYPE = (
    ('1', 'Full Time'),
    ('2', 'Part Time'),
    ('3', 'Intership')
)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Job(models.Model):
    user = models.ForeignKey(User, related_name="User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    category = models.ForeignKey(Category,related_name='Category', on_delete=models.CASCADE)
    salary = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200)
    company_description = models.TextField()
    company_url = models.URLField(max_length=200)
    last_date = models.DateField()
    is_published = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=12, blank=True)
    resume = models.FileField(upload_to="employee/resumes", default="")
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.job.title


class ApplyJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.user.email
    
class SaveJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.job.title
    
    