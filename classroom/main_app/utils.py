from django.contrib import messages
from django.http import request
from .models import *
from .forms import *

def user_profile(request):
    if request.user.is_admin or request.user.is_superuser:
        user          = Admins.objects.get(user=request.user)
        admins        = Admins.objects.all()
        teachers      = Teachers.objects.all()
        students      = Students.objects.all()
        courses       = Courses.objects.all()        
        # notifications = Notifications.objects.all()
        events        = Events.objects.filter().all()

    elif request.user.is_teacher:
        user          = Teachers.objects.get(user=request.user)
        admins        = Admins.objects.all()
        teachers      = Teachers.objects.all()        
        courses       = Courses.objects.filter(course=user.courses).all()        
        students      = Students.objects.filter(courses=courses).all()
        # notifications = Notifications.objects.filter(course=user.courses).all()
        events        = Events.objects.filter().all()  

    elif request.user.is_student:        
        user          = Students.objects.get(user=request.user)
        admins        = Admins.objects.all()
        teachers      = Teachers.objects.all()
        students      = Students.objects.filter(year=user.year).all()
        courses       = Courses.objects.filter(year=user.year).all()
        # notifications = Notifications.objects.filter(year=user.year).all()
        events        = Events.objects.filter().all()

    return {'user':user,'courses':courses,'admins':admins,'teachers':teachers,'students':students,'events':events} 

def create_teacher(user_form,form):
    user_form.instance.is_teacher = True    
    user_form.save()
    email = user_form['email'].value            
    user   = UserAccount.objects.get(email=email)             
    form.instance.user = user
    form.save()  
    
def create_admin(user_form,form):
    user_form.instance.is_admin = True
    user_form.instance.is_staff = True
    user_form.save()
    # group  = Group.objects.get(name='Admins')
    # user_form.instance.groups.add(group)
    user   = UserAccount.objects.get(email=user_form['email'].value())             
    form.instance.user = user
    form.save()   
