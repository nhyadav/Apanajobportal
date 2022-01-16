from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UserDetailForm, JobForm, JobEditForm, JobApplyForm
from .models import UserDetails, Category, Job, Applicant, SaveJob, ApplyJob
from django.contrib import messages


# Create your views here.
@login_required(login_url='/login')
def jobs(request):
    
    full_time = []
    part_time = []
    intership = []
    jobs = Job.objects.filter(is_published=True)
    if request.user.is_staff:
        user = get_object_or_404(User, id=request.user.id)
        employer_job = Job.objects.filter(user=user)

        context = {
            'employer_job': employer_job
            }
    else:
        for job in jobs:
            
            if job.job_type == 1 :
                full_time.append(job)
            elif job.job_type == 2 :
                part_time.append(job)
            else:
                intership.append(job)

        context = {
            'full_time': full_time,
            'part_time': part_time,
            'internship': intership,
        }
    return render(request, 'job/jobspage.html', context=context)


@login_required(login_url='/login')
def profile(request):
    user = get_object_or_404(User,id=request.user.id)
    user_data  = UserDetails.objects.all().filter(user=user)
    name = request.user.first_name + request.user.last_name
    if user_data:
        user_details = user_data[0]
        context = {
            'name': name,
            'user_data': user_details
            }
        return render(request, 'job/profile.html', context=context)
    else:
        form = UserDetailForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                messages.success(request, "your details have been successfully taken....")
                return redirect('profile')
            else:
                messages.error(request, form.errors)
                return render(request, 'job/profile.html')

        context = {
            'form': form,
            'guest': True,
            'name': name
        }
        return render(request, 'job/profile.html', context=context)

@login_required(login_url="/login")
def edit_profile(request, id):
    user = get_object_or_404(UserDetails, id=id, user=request.user.id)
    form = UserDetailForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, "User Details have successfully updated!...")
        return redirect('/profile')
    context = {
        'form': form
    }
    return render(request, 'job/profiledit.html', context=context)



#create new job
@login_required(login_url='/login')
def job_create(request):
    form = JobForm(request.POST)
    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            messages.success(request, "Your job is created successfully.")
            return redirect('jobs')
        else:
            messages.error(request, form.errors)
    context = {
        'form':form,
        'categories': categories
    }
    return render(request, 'job/jobcreate.html', context=context)



@login_required(login_url='/login')
def job_edit(request, id):
    job = get_object_or_404(Job, id=id)
    form = JobEditForm(request.POST, instance=job)
    categories = Category.objects.all()
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Your Job details has been updated...")
            return redirect('jobs')
        else:
            messages.error(request, form.errors)
    
    context = {
        'form': form,
        'categories':categories,
        'job':job
    }
    return render(request, "job/jobedit.html", context=context)


@login_required(login_url='/login')
def job_view(request, id):
    job = get_object_or_404(Job, id=id)
    context = {
        'job':job
    }
    return render(request, 'job/jobview.html', context=context)

@login_required(login_url='/login')
def deletejob(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)
    if job:
        job.delete()
        messages.success(request, "Your job has been deleted.")
    return redirect('jobs')

@login_required(login_url="/login")
def publishjob(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)
    if job.is_published:
        job.is_published = False
        job.save()
    else:
        job.is_published = True
        job.save()
    return redirect('jobs')

@login_required(login_url="/login")
def applyjob(request, jobid):
    user = get_object_or_404(User, id=request.user.id)
    form = JobApplyForm(request.POST, request.FILES)
    applicant = Applicant.objects.filter(user=user, job=jobid)
    job = get_object_or_404(Job,id=jobid)

    if not applicant:
        if request.method == "POST":
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.job = job
                instance.save()
                applyjob = ApplyJob.objects.create(user=user,job=job)
                applyjob.save()
                messages.success(request, "You have apply for this job.")
                return redirect("viewjob", jobid)
            else:
                messages.error(request, form.errors)
                return render(request, "job/jobapply.html")
    else:
        messages.error(request, "You have already applied for this job")
        return redirect("viewjob", jobid)

    context = {
        'form':form
    }
    return render(request, "job/jobapply.html", context=context)

@login_required(login_url="/login")
def savejob(request, jobid):
    user = get_object_or_404(User, id=request.user.id)
    job = get_object_or_404(Job, id=jobid)
    sjob = SaveJob.objects.filter(user=user,job=job)
    if not sjob:
        savejob = SaveJob.objects.create(user=user,job=job)
        savejob.save()
        messages.success(request, "Your job have been saved for you.")
        return redirect('viewjob', jobid)
    else:
        messages.error(request, "You have already saved this job.")
        return redirect("viewjob", jobid)
