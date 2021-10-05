from django.contrib import messages
from django.db.models.query_utils import Q
from django.http import request
from django.shortcuts import redirect
from .models import *
from .forms import *

def user_profile(request):
    if request.user.is_admin or request.user.is_superuser:
        user          = Admins.objects.get(user=request.user)
        admins        = Admins.objects.all()
        teachers      = Teachers.objects.all()
        students      = Students.objects.all()
        courses       = Courses.objects.all()
        group         = Group.objects.get(name='Admins')        
        notifications = Notifications.objects.filter(Q(receivers=group) | Q(unique_receiver=request.user)).order_by('-created').all()
        
        events        = Events.objects.all()

    elif request.user.is_teacher:
        user          = Teachers.objects.get(user=request.user)
        admins        = Admins.objects.all()
        teachers      = Teachers.objects.all()        
        courses       = Courses.objects.get(name=user.course)    
        students      = Students.objects.filter(year=courses.year).all()
        group         = Group.objects.get(name='Teachers')
        notifications = Notifications.objects.filter(Q(receivers=group,year=courses.year) | Q(unique_receiver=request.user)).order_by('-created').all()
        
        events        = Events.objects.filter(year=courses.year).all()  

    elif request.user.is_student:        
        user          = Students.objects.get(user=request.user)
        admins        = Admins.objects.all()
        teachers      = Teachers.objects.all()
        students      = None
        courses       = Courses.objects.filter(year=user.year).all()
        group         = Group.objects.get(name='Students')
        notifications = Notifications.objects.filter(Q(receivers=group,year=user.year) | Q(unique_receiver=request.user)).order_by('-created').all()
        
        events        = Events.objects.filter(year=user.year).all()

    return {'user':user,'courses':courses,'admins':admins,'teachers':teachers,'students':students,'events':events,'notifications':notifications,} 

def create_teacher(user_form,form):
    user_form.instance.is_teacher = True       
    user_form.save() 
    group  = Group.objects.get(name='Teachers')
    user_form.instance.groups.add(group)   
    email = user_form['email'].value            
    user   = UserAccount.objects.get(email=email)             
    form.instance.user = user
    form.save()  
    
def create_admin(user_form,form):
    user_form.instance.is_admin = True
    user_form.instance.is_staff = True
    user_form.save()
    group  = Group.objects.get(name='Admins')
    user_form.instance.groups.add(group)
    user   = UserAccount.objects.get(email=user_form['email'].value())             
    form.instance.user = user
    form.save()   

def create_student(user,admission):
    from django.core.files import File 
    Students.objects.create(
        user          = user,              
        document      = admission.document,
        first_name    = admission.first_name,
        last_name     = admission.last_name,
        date_of_birth = admission.date_of_birth,
        gender        = admission.gender,
        nationality   = admission.nationality,
        year          = admission.year, 
        profile_picture = File(admission.profile_picture), 
        HS_diploma      = File(admission.HS_diploma)         
    )
    
    
 
def request_account(request):
    data = user_profile(request)
    user = data['user']

    if request.user.is_admin:
        admissions   = Applications.objects.order_by('-sent_date').all()
        history      = None
        classwork    = None 
        studentworks = None        

    if request.user.is_student:
        history      = History.objects.order_by('-seen')[0:5]   
        admissions   = None 
        classwork    = ClassWork.objects.filter(year=user.year).all() 
        studentworks = None  
        
    elif request.user.is_teacher:
        classwork    = ClassWork.objects.filter(course=user.course).all()
        studentworks = StudentWorks.objects.filter(course=user.course).order_by('-id').all()
        admissions   = None 
        history      = None  
     

    return{'classwork':classwork,'admissions':admissions,'history':history,'studentworks':studentworks}    
        