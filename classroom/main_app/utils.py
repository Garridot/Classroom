from .models import *
from .forms import *
from calendar import HTMLCalendar
from users.models import *

class GetCalendar():
    def calendar():
        year     = timezone.now().year
        month    = timezone.now().month
        calendar = HTMLCalendar().formatmonth(theyear=year,themonth=month) 
        return calendar

class UserObjs():   

    def request_user(user):
        user = UserAccount.objects.get(email=user)
        user_request = {}
        
        
        if user.groups.all()[0].name == 'Students':                        
            student = Students.objects.get(user=user)
            

            user_request['title1'] = 'Seen recently '
            
            list1  = History.objects.filter(student=student).order_by('-seen')[0:5]
            user_request['title2'] = 'Homework'  
            course = Courses.objects.filter(year=student.year)           
            list2  = School_Assignment.objects.filter(topic__in=Topic.objects.filter(course__in=course))[0:5]

        elif user.groups == 'Teachers':
            teacher = Teachers.objects.get(user=user)
            

            user_request['title1'] = 'School assignment'
            list1  = School_Assignment.objects.filter(course=teacher.course)[0:5]   
            user_request['title2'] = 'Homework' 
            list2  = Students_Assignment.objects.filter()[0:5]  

        else:
            
            user_request['title1']  = 'Students'            
            list1  = Students.objects.all()[0:5]
            user_request['title2']  = 'Teachers'
            list2  = Teachers.objects.all()[0:5] 

        return {'user_request':user_request,'list1':list1,'list2':list2}     
              
class Create_Teacher():
    def create(form,form_kwargs):         
        form.save()
        email = form['email'].value()    
        form_kwargs.instance.user = UserAccount.objects.get(email = email)             
        form_kwargs.save() 
               

class Create_Student():
    def create(form,form_kwargs):
        form.instance.is_student = True    
        form.save()    
        form_kwargs.instance.user = UserAccount.objects.get(email= form['email'])             
        form_kwargs.save()     

