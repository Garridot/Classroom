from django.http import request
from classroom.settings  import  EMAIL_HOST_USER

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import send_mail

from django.contrib.auth import login, logout , authenticate
from django.shortcuts import render,redirect
from django.contrib import messages
from calendar import HTMLCalendar


from .models import * 
from .forms import *
from .utils import *
from .filters import*

# Create your views here.

def MainPage(request):
    return render(request,'main_page.html')
def Information(request):
    return render(request,'information.html')
def Contact(request):    
    if request.method == 'POST':
        name    = request.POST['name']
        email   = request.POST['email']
        message = request.POST['message']
        send_mail(
            'Message from' + name,
            message,
            email,
            [EMAIL_HOST_USER],
        )
        return render(request,'contact.html',{'name':name}) 
    return render(request,'contact.html',{}) 


def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')        
        user = authenticate(request , email = email, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')            
        else:           
            messages.info(request,'Email or password is incorrect.') 
    return render(request,'login.html')
def LogoutView(request):     
    logout(request)
    return redirect('login') 


def PasswordReset(request):
    if request.method == 'POST':
        email = request.POST['email']        
        user = UserAccount.objects.filter(email=email)        
        if user:
            user = UserAccount.objects.get(email=email)  
            PasswordResetEmail(user)
            return redirect('password_reset_email_sent')
                       
        else:            
           messages.info(request,'Email not found.') 
    return render(request,'password_reset/password_reset.html')
def PasswordResetEmail(user): 
    from django.contrib.auth.tokens import PasswordResetTokenGenerator
    password_reset_token = PasswordResetTokenGenerator().make_token(user)   
    context = {'user':user,'token':password_reset_token}
    template  = get_template('password_reset/password_reset_email.html')
    content   = template.render(context)
    email     = EmailMultiAlternatives(
        'AcademiaWeb',
        'Password Reset',
        EMAIL_HOST_USER,
        [user.email]
    )
    email.attach_alternative(content,'text/html')
    email.send()
def PasswordResetEmailSent(request):
     return render(request,'password_reset/password_reset_email_sent.html')             
def PasswordResetForm(request,email,token):
    user = UserAccount.objects.get(email= email)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():                     
            form.save()            
            return redirect('password_reset_done',email=email)
        else:
            for msg in form.errors:
                messages.info(request,f"{msg}:{form.errors}")
    return render(request,'password_reset/password_reset_form.html',{'form':form})                
def PasswordResetDone(request,email):
    return render(request,'password_reset/password_reset_done.html',{'email':email})

def ApplicationsFormView(request):
    form = ApplicationsForm()
    if request.method == 'POST':
        form = ApplicationsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            ApplicationSendEmail(email=form.instance.email)            
            return redirect('application_send',pk=form.instance.email)
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}")   
    context={'form':form}
    return render(request,'form.html',context)  
def ApplicationSend(request,pk):
    admission = Applications.objects.get(email=pk)
    context={'admission':admission}
    return render(request,'application_send.html',context) 
def ApplicationSendEmail(email):
    admission = Applications.objects.get(email=email)  
    context   = {'email':email,'admission':admission}     
    template  = get_template('emails/application_send_email.html')
    content   = template.render(context)

    email     = EmailMultiAlternatives(
        'Request received!',
        'Your application has been successfully submitted.',
        EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(content,'text/html')
    email.send()

def HomeView(request):
    data = user_profile(request)
    user = data['user']
    notifications = Notifications.objects.all()

    year     = timezone.now().year
    month    = timezone.now().month
    calendar = HTMLCalendar().formatmonth(theyear=year,themonth=month) 
    events   = Events.objects.filter(event_date__month=month).all()  

    if request.user.is_admin:
        info = Applications.objects.order_by('-sent_date').all()
    

    context = {'notifications':notifications,
        'user':user,'calendar':calendar,'info':info,
        'events':events,        
    }

    return render(request,'home.html',context) 

def UserProfileView(request,full_name):
    data = user_profile(request)
    user = data['user']
    context = {'user':user}
    return render(request,'profile.html',context)

def AdmissionsView(request):
    data = user_profile(request)
    user = data['user']

    requests = Applications.objects.all()
    filters  = ApplyFilters(request.GET,queryset=requests)
    requests = filters.qs     
    title    = 'Admissions'
    request_data = 'admission_data'      
    context  = {'requests':requests,'filters':filters,'title':title,'request_data':request_data,'user':user}
    return render(request,'request_list.html',context)
def AdmissionData(request,email):
    admission = Applications.objects.get(email=email)   
    context = {'admission':admission}
    return render(request,'admission_profile.html',context)
def AdmissionAccept(request,email):
    admission = Applications.objects.get(email=email)     
    info = f'The student needs a password.\nTips:\nemail: {admission.email}\npassword: {admission.first_name}{admission.last_name}{admission.document}'
    form = UserForm()
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            AdmissionEMAIL(email)
            admission.delete()
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 
    context = {'info':info,'form':form}
    return render(request,'form.html',context)
def AdmissionEMAIL(email):
    admission = Applications.objects.get(email=email)  
    context   = {'email':email,'admission':admission}     
    template  = get_template('emails/application_accepted.html')
    content   = template.render(context)

    email     = EmailMultiAlternatives(
        f'Congratulations {admission.full_name}!',
        'Your application has been successfully accepted.',
        EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(content,'text/html')
    email.send()
def AdmissionDenied(email): 
    admission = Applications.objects.get(email=email)  
    context   = {'email':email,'admission':admission}     
    template  = get_template('emails/application_denied.html')
    content   = template.render(context)

    email     = EmailMultiAlternatives(
        'Student not chosen',
        'Your application has been successfully denied.',
        EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(content,'text/html')
    email.send()       

def StudentsView(request):
    data = user_profile(request)
    user = data['user']
    requests = Students.objects.all()
    filters  = StudentsFilters(request.GET,queryset=requests)
    requests = filters.qs     
    title    = 'Students'
    request_data = 'student_data'      
    context  = {'requests':requests,'filters':filters,'title':title,'request_data':request_data,'user':user}
    return render(request,'request_list.html',context)
    
  