from unicodedata import name
from .models import *
from .forms import *
from calendar import HTMLCalendar
from users.models import *


class GetAccount():
    def get(user):
        if Students.objects.filter(user=user).exists(): return Students.objects.get(user=user)
        elif Teachers.objects.filter(user=user).exists(): return Teachers.objects.get(user=user)
        else: return None
        

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

        elif user.groups.all()[0].name == 'Teachers':
            teacher = Teachers.objects.get(user=user)
            

            user_request['title1'] = 'School assignment'
            topic  = Topic.objects.filter(course=teacher.course).all() 
            
            list1  = School_Assignment.objects.filter(topic__in=topic)[0:5]  
            user_request['title2'] = 'Homework' 
            list2  = Students_Assignment.objects.filter(assignment__in=list1)[0:5]  

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
        user = UserAccount.objects.get(email = email) 

        group = Group.objects.get(name='Teachers')        
        user.groups.add(group)

        form_kwargs.instance.user = user             
        form_kwargs.save() 
               

class Create_Student():
    def create(form,form_kwargs):
        form.instance.is_student = True    
        form.save() 
        
        email = form['email'].value() 
        user = UserAccount.objects.get(email = email)

        group = Group.objects.get(name='Students')
        user.groups.add(group)

        group.user_set.add(UserAccount.objects.get(email= form['email']))
          

        form_kwargs.instance.user = UserAccount.objects.get(email= form['email'])             
        form_kwargs.save()     

