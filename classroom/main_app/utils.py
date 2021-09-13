from .models import *

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


