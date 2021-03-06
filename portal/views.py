from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from jobportal import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, logout, login as dj_login
from . token import generate_token
from job.models import Job, SaveJob,Applicant,ApplyJob
import logging

# configure the logging for creating log file
logging.basicConfig(filename="logging\\jobseeker\\userlogging.txt",
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG
                    )
logging.info("JOBSEEKER is ready to use for users.")
# Create your views here.
def home(request):
    return render(request, 'portal/index.html')


####login############
def login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                dj_login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Bad Credintials')
                logging.error("Bad Credintials")
    except Exception as exp:
        logging.error(exp)

    return render(request,'portal/login.html')


#########signup##########
def signup(request):
    if request.method == 'POST':
        role = request.POST['role']
        try:
            if role == "Employer":
                firstname = request.POST['fname']
                lastname = request.POST['lname']
                email = request.POST['email']
                password = request.POST['password']
                password2 = request.POST['repsw']
        

                if password == password2:
                    emp = User.objects.create_superuser(username=email,email=email,password=password)
                    emp.first_name = firstname
                    emp.last_name = lastname
                    emp.is_active = False
                    emp.save()
                    messages.success(request,"Your Account is created. Please! check your email for confirmation email id.")
                    logging.info("Account is created")

                    #welcome email
                    subject = 'Welcome in jobportal'
                    message = 'Hello'+ emp.first_name+emp.last_name+' Welcome in jobportal!! \nThank for visiting our site. \nWe have also sent you a conformation email, please confirm the email. \n\nThanking You \n nvr'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [emp.email]
                    send_mail(subject, message, from_email,to_list, fail_silently=True)

                    #email confirmation
                    current_site = get_current_site(request)
                    email_subject = "Confirmation for email address in jobportal"
                    message2 = render_to_string('portal/email_confirmation.html',
                    {
                        'name': emp.first_name+emp.last_name,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(emp.pk)),
                        'token': generate_token.make_token(emp)
                    })
                    email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [emp.email],
                    )
                    email.fail_silently = True
                    email.send()

                    return redirect('login')
                
                else:
                    error = "Your password are not maching..."
                    messages.error(request, error)
                    logging.error(error)
                    return redirect('signup')
                    

                if User.objects.filter(username=email):
                    error = "Username and email id is already existing.!!"
                    messages.error(request, error)
                    logging.error(error)
                    return redirect('signup')

            else:
                firstname = request.POST['fname']
                lastname = request.POST['lname']
                email = request.POST['email']
                password = request.POST['password']
                password2 = request.POST['repsw']
                

                if password == password2:
                    emp = User.objects.create_user(username=email,email=email,password=password)
                    emp.first_name = firstname
                    emp.last_name = lastname
                    emp.is_active = False
                    emp.save()
                    messages.success(request,"Your Account is created. Please! check your email for confirmation email id.")
                    logging.info("employee account is created")
                    #welcome email
                    subject = 'Welcome in jobportal'
                    message = 'Hello '+ emp.first_name+emp.last_name+' Welcome in jobportal!! \nThank for visiting our site. \nWe have also sent you a conformation email, please confirm the email. \n\nThanking You \n nvr'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [emp.email]
                    send_mail(subject, message, from_email,to_list, fail_silently=True)

                    #email confirmation
                    current_site = get_current_site(request)
                    email_subject = "Confirmation for email address in jobportal"
                    message2 = render_to_string('portal/email_confirmation.html',
                    {
                        'name': emp.first_name+emp.last_name,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(emp.pk)),
                        'token': generate_token.make_token(emp)
                    })
                    email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [emp.email],
                    )
                    email.fail_silently = True
                    email.send()
                    return redirect('login')
                else:
                    error = "Your password are not maching..."
                    messages.error(request, error)
                    logging.error(error)
                    return redirect('signup')
        

                if User.objects.filter(username=email):
                    error = "Username and email id is already existing.!!"
                    messages.error(request, error)
                    logging.error(error)
                    return redirect('signup')
        except Exception as ex:
            messages.error(request, ex)
            error = "Something went wrong!..."
            logging.error(ex)
            return redirect('signup')
        
    return render(request, 'portal/signup.html')



###############activate account#############
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        dj_login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        logging.error("Your account is activated")
        return redirect('login')
    else:
        logging.error("failed to account to activate")
        return render(request,'activation_failed.html')



###########logout account##########
def signout(request):
    logout(request)
    messages.success(request,'logout successfully!!')
    logging.info("successfully logout..")
    return redirect('home')


###########dashboard######
def dashboard(request):
    #employer
    user = get_object_or_404(User,id=request.user.id)
    if request.user.is_staff:
        jobs = Job.objects.filter(user=user, is_published=True)
        applicants=[]
        for job in jobs:
            applicant = Applicant.objects.filter(job=job)
            if applicant:
                applicants.append(applicant)
                
        
        context={
                    'name': request.user.first_name,
                    'is_authenticated': request.user.is_authenticated,
                    'is_staff': request.user.is_staff,
                    'jobs':jobs,
                    'applicants':applicants
                }
    

    #employee
    else:
        savedjob = SaveJob.objects.filter(user=user)
        applyedjob = ApplyJob.objects.filter(user=user) 
        context = {
            'name': request.user.first_name,
            'is_authenticated': request.user.is_authenticated,
            'is_staff': request.user.is_staff,
            'savedjob': savedjob,
            'applyedjob': applyedjob,
        }
    return render(request, 'portal/home.html', context=context)