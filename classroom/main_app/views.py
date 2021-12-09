from django.contrib.auth.forms import UserChangeForm
from django.http import request
from django.http.response import HttpResponse
from classroom.settings  import  EMAIL_HOST_USER

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import send_mail

from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth.decorators import login_required


from django.shortcuts import render,redirect
from django.contrib import messages
from calendar import HTMLCalendar
from django.http import JsonResponse

from django.views import View


from .models import * 
from .forms import *
from .utils import *
from .filters import*
from .decorators import *


import json


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


# Register
def ApplicationsFormView(request):
    user_form = UserForm()
    form = StudentsForm()
    title = 'Apply Form'
    if request.method == 'POST':
        form = StudentsForm(request.POST,request.FILES)
        user_form = UserForm(request.POST)
        if form.is_valid() and user_form.is_valid():

            user_form.save()
            form.instance.user = UserAccount.objects.get(email=user_form.instance.email)
            form.save()            
            AdmissionEMAIL(email=user_form.instance.email)
            return redirect('login')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}")  
    context={'form':form,'title':title,'user_form':user_form}    
    return render(request,'form.html',context)  

def AdmissionEMAIL(email):
    admission = UserAccount.objects.get(email=email)  
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



def RecentContent(request):
    from django.utils import timezone 
    data = json.load(request)['content']
    content_json = data   
    if request.user.is_student:        
        student = Students.objects.get(user=request.user)
        content = Content.objects.get(id=content_json)
        try:
            hitorial  = History.objects.get(student=student,content_id=content)
            if hitorial:
                History.objects.filter(student=student,content_id=content).update(seen=timezone.now())
        except:              
            History.objects.create(student=student,content_id=content,topic_id=content.topic,course_id=content.topic.course)

    return JsonResponse(data,safe=False)   





@login_required(login_url='login')
def HomeView(request):
    data = user_profile(request)    
    user = data['user']
    notifications = data['notifications']
    
    
    year     = timezone.now().year
    month    = timezone.now().month
    calendar = HTMLCalendar().formatmonth(theyear=year,themonth=month) 
    events   = Events.objects.filter(event_date__month=month).all() 
    
    classworks   = request_account(request)['classwork']
    admissions   = request_account(request)['admissions']
    history      = request_account(request)['history']
    studentworks = request_account(request)['studentworks']

    
    
    context = {'notifications':notifications,
                'user':user,'calendar':calendar,'events':events,
                'classworks':classworks,'admissions':admissions,  
                'history':history,'studentworks':studentworks
                     
    }
    return render(request,'home.html',context) 

@login_required(login_url='login')
@allowed_user(allowed_roles=['Students'])
def GradesView(request,email):
    data = user_profile(request)    
    user = data['user']
    notifications = data['notifications']
    student = Students.objects.get(user=request.user)
    works   = StudentWorks.objects.filter(student=student).all() 
    passeds = StudentWorks.objects.filter(student=student,status='Passed').all().count()
    faileds = StudentWorks.objects.filter(student=student,status='Failed').all().count()    
    total_works = 0
    for w in works:
        total_works += 1        
    grades = 0    
    for g in works:
        grades += g.grade 

    average = (int(grades)/int(total_works)) 
    average = round(average, 1)
          
    context = {'student':student,'works':works,'average':average,'notifications':notifications,
                'user':user,'passeds':passeds,'faileds':faileds }    
    return render(request,'grades.html',context) 

@login_required(login_url='login')
@allowed_user(allowed_roles=['Students'])
def GradeData(request,work_id):
    work = StudentWorks.objects.get(id=work_id)
    context = {'work':work}
    return render(request,'my_work.html',context)

@login_required(login_url='login')
def UserProfileView(request,email):
    data = user_profile(request)
    user = data['user']
    update_url = f'/academiaweb/user_profile_update/email={user.email}/'
    context = {'user':user,'update_url':update_url}
    return render(request,'profile.html',context)
@login_required(login_url='login')
def UserProfileUpdate(request,email):
    import os
    from django.core.files import File 
    user = UserAccount.objects.get(email=email) 
    data = user_profile(request)
    account = data['user']
    form    = UpdateUserForm(instance=user)
    if request.method == 'POST':
        form  = UpdateUserForm(request.POST,instance=user)
        profile_picture = request.FILES['profile_picture']
        if form.is_valid():       
            form.save()
            if len(profile_picture)!= 0:
                if len(profile_picture)> 0:
                    os.remove(account.profile_picture.path)
                account.profile_picture = request.FILES['profile_picture']
            account.save()
            messages.success(request,'Account successfully update!')
            return redirect('home')
    context = {'user':user,'account':account,'form':form}
    return render (request,'user_update_form.html',context)                

@login_required(login_url='login')
def PasswordsChange(request,email):
    user  = UserAccount.objects.get(email=email)
    form  = PasswordChangeForm(user=user)
    title = 'Password Change' 
    if request.method == 'POST':
        form  = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():       
            form.save()            
            return redirect('login')
        else: 
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 
    context = {'form':form,'title':title}
    return render(request,'form.html',context)        





@login_required(login_url='login')
def StudentsView(request):
    data = user_profile(request)
    user = data['user']
    students = Students.objects.all()
    filters  = StudentsFilters(request.GET,queryset=students)
    students = filters.qs     
    title    = 'Students'         
    context  = {'students':students,'filters':filters,'title':title,'user':user}
    return render(request,'request_list.html',context)
@login_required(login_url='login')
def StudentData(request,email):
    user = UserAccount.objects.get(email=email)
    user = Students.objects.get(user = user)
    update_url = f'/academiaweb/students/student_update/email={user.email}'
    delete_url = f'/academiaweb/students/student_delete/email={user.email}'
    context = {'user':user,'update_url':update_url,'delete_url':delete_url}
    return render(request,'profile.html',context)
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def StudentUpdate(request,email):
    user = UserAccount.objects.get(email=email)
    student = Students.objects.get(user = user)
    form = StudentsForm(instance=student)
    title = 'Update Student'
    if request.method == 'POST':
        form = StudentsForm(request.POST,request.FILES,instance=student)
        if form.is_valid():
            form.save()
            messages.success(request,'Student successfully updated')
            return redirect('students')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}")   
    context = {'form':form,'title':title}
    return render (request,'form.html',context)                
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def StudentDelete(request,email): 
    user = UserAccount.objects.get(email=email)
    user.delete()
    messages.success(request,'Student successfully deleted')
    return redirect('students')



  

@login_required(login_url='login')
def TeachersView(request):  
    data = user_profile(request)
    user = data['user']
    teachers = Teachers.objects.all()
    filters  = TeachersFilters(request.GET,queryset=teachers) 
    teachers = filters.qs     
    title    = 'Teachers'     
    create_url   =  'teacher_create'         
    context  = {'teachers':teachers,'filters':filters,'title':title,'user':user,'create_url':create_url}
    return render(request,'request_list.html',context)    
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def TeacherCreate(request):
    user_form = UserForm()
    title     = 'Add Teacher Account'
    form     = TeachersForm()
    if request.method == 'POST':
        form = TeachersForm(request.POST,request.FILES)
        user_form = UserForm(request.POST)
        if form.is_valid() and user_form.is_valid(): 
            user_form.instance.is_teacher = True    
            user_form.save()
            email = user_form['email'].value()            
            user   = UserAccount.objects.get(email=email)             
            form.instance.user = user
            form.save()              
            messages.success(request,'Teacher created successfully.')
            return redirect('teachers')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 

    context = {'form':form,'user_form':user_form,'title':title}
    return render (request,'form.html',context) 
@login_required(login_url='login')
def TeacherData(request,email):
    user_teacher  = UserAccount.objects.get(email=email)
    teacher_account = Teachers.objects.get(user=user_teacher)
    update_url = f'/academiaweb/teachers/teacher_update/email={user_teacher.email}/'
    delete_url = f'/academiaweb/teachers/teacher_delete/email={user_teacher.email}/'
    context = {'user':teacher_account,'update_url':update_url,'delete_url':delete_url}
    return render(request,'profile.html',context)
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def TeacherUpdate(request,email):
    user = UserAccount.objects.get(email=email)
    teachers = Teachers.objects.get(user = user)
    form = TeachersForm(instance=teachers)
    title = 'Update Teachers'
    if request.method == 'POST':
        form = TeachersForm(request.POST,request.FILES,instance=teachers)
        if form.is_valid():
            form.save()
            messages.success(request,'Teacher successfully updated')
            return redirect('teachers')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}")   
    context = {'form':form,'title':title}
    return render (request,'form.html',context)    
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def TeacherDelete(request,email):
    user  = UserAccount.objects.get(email=email)
    user.delete()
    messages.success(request,'Teacher deleted successfully.')
    return redirect('teachers')  


@login_required(login_url='login')
def AdminsView(request):
    data = user_profile(request)
    user = data['user']
    admins  = Admins.objects.all()
    filters = AdminsFilters(request.GET,queryset=admins) 
    admins  = filters.qs
    title   = 'Admins'
    create_url = 'admin_create'
    context  = {'admins':admins,'filters':filters,'title':title,'user':user,'create_url':create_url}
    return render(request,'request_list.html',context)    
@login_required(login_url='login')
def AdminsData(request,email):
    user  = UserAccount.objects.get(email=email)
    user  = Admins.objects.get(user=user)
    update_url = f'/academiaweb/admins/admin_update/email={user.email}/'
    delete_url = f'/academiaweb/admins/admin_delete/email={user.email}/'
    context = {'user':user,'update_url':update_url,'delete_url':delete_url}
    return render(request,'profile.html',context)
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def AdminUpdate(request,email):
    user = UserAccount.objects.get(email=email)
    admin = Admins.objects.get(user = user)
    form = AdminsForm(instance=admin)
    title = 'Update Admins'
    if request.method == 'POST':
        form = AdminsForm(request.POST,request.FILES,instance=admin)
        if form.is_valid():
            form.save()
            messages.success(request,'Admin successfully updated')
            return redirect('admins')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}")   
    context = {'form':form,'title':title}
    return render (request,'form.html',context)
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def AdminCreate(request):
    user_form = UserForm()
    title     = 'Add Teacher Account'
    form      =  AdminsForm()
    if request.method == 'POST':
        form = AdminsForm(request.POST,request.FILES)
        user_form = UserForm(request.POST)
        if form.is_valid() and user_form.is_valid(): 
            user_form.instance.is_admin = True    
            user_form.save()
            email = user_form['email'].value()            
            user   = UserAccount.objects.get(email=email)             
            form.instance.user = user
            form.save()              
            messages.success(request,'Admin successfully created.')
            return redirect('admins')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 

    context = {'form':form,'user_form':user_form,'title':title}
    return render (request,'form.html',context) 
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def AdminDelete(request,email): 
    user = UserAccount.objects.get(email=email)
    user.delete()
    messages.success(request,'Admin successfully deleted')
    return redirect('admins')


@login_required(login_url='login')
def CoursesView(request):
    data = user_profile(request)
    user = data['user']
    courses = Courses.objects.all()
    filters  = CoursesFilters(request.GET,queryset=courses) 
    courses = filters.qs     
    title    = 'Courses'     
    create_url   =  'course_create'     
    context  = {'courses':courses,'filters':filters,'title':title,'user':user,'create_url':create_url}
    return render(request,'request_list.html',context)  
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def CourseCreate(request):    
    form     = CoursesForm()
    title    = 'Create Course'
    if request.method == 'POST':
        form     = CoursesForm(request.POST,request.FILES)        
        if form.is_valid(): 
            form.save()
            messages.success(request,'Course successfully created.')
            return redirect('courses')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 
    context = {'form':form,'title':title}        
    return render (request,'form.html',context)
@login_required(login_url='login')
def CourseData(request,name,year):
    course = Courses.objects.get(name=name,year=year)
    teachers = Teachers.objects.filter(course=course).all()
    if request.user.is_teacher:
        if Teachers.objects.get(user =request.user).course == course:            
            teacher_course = True
        else:
            teacher_course = False  
    else:
            teacher_course = False 
    topics  = CourseTopic.objects.filter(course=course).all()     
    context =  {'course':course,'teachers':teachers,'topics':topics,'teacher_course':teacher_course}
    return render(request,'course_data.html',context)
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def CourseUpdate(request,name,year):
    course = Courses.objects.get(name=name,year=year)
    form   = CoursesForm(instance=course)
    title  = 'Update Course'
    if request.method=='POST':
        form = CoursesForm(request.POST,request.FILES,instance=course)
        if form.is_valid():
            form.save()            
            return redirect('course',name=course.name,year=course.year)
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 
    context = {'form':form,'title':title}        
    return render (request,'form.html',context)    
@login_required(login_url='login')
def CourseDelete(request,name,year):
    course = Courses.objects.get(name=name,year=year)    
    course.delete()
    messages.success(request,'Course successfully deleted.')
    return redirect('courses') 


@login_required(login_url='login')
def TopicsView(request,course,topic):
    course   = Courses.objects.get(name=course)
    if request.user.is_teacher:
        if Teachers.objects.get(user =request.user).course == course:           
            teacher_course = True
        else:
            teacher_course = False  
    else:
            teacher_course = False 
    topic = CourseTopic.objects.get(course = course,name=topic)
    contents  = Content.objects.filter(topic=topic).all()
    assignments  = ClassWork.objects.filter(topic=topic).all()
    context  = {'course':course,'teacher_course':teacher_course,'topic':topic,'contents':contents,'assignments':assignments,'teacher_course':teacher_course}
    return render(request,'topic_data.html',context) 
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def TopicCreate(request,course):
    course = Courses.objects.get(name=course)
    form   = TopicForm()
    title  = 'Add Topic'
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.instance.course = course
            form.instance.year   = course.year
            form.save()
            group  = Group.objects.get(name='Students')
            Notifications.objects.create(message=f"{course.name} : New topic has been added!",receivers=group,year=course.year) 
            return redirect('course', course.name, course.year)
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 
    context= {'form':form,'title':title}
    return render(request,'form.html',context) 
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def TopicUpdate(request,course,topic):
    course   = Courses.objects.get(name=course)
    topic    = CourseTopic.objects.get(course = course,name=topic)
    form     = TopicForm(instance=topic)
    title    = 'Update Topic'
    if request.method == 'POST':
        form = TopicForm(request.POST,instance=topic)
        if form.is_valid():
            form.save()
            return redirect('course',name=course.name,year=course.year)
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}")     
    context = {'form':form,'title':title}        
    return render (request,'form.html',context)               
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def TopicDelete(request,course,topic):
    course   = Courses.objects.get(name=course)
    topic    = CourseTopic.objects.get(course = course,name=topic)
    topic.delete()
    return redirect('course',name=course.name,year=course.year)


@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def ContentAdd(request,course,topic):
    topic    = CourseTopic.objects.get(name=topic)
    course   = Courses.objects.get(name=course)
    form  = ContentForm()
    title = 'Add content'
    if request.method == 'POST':
        form = ContentForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.topic = topic
            form.save()
            group  = Group.objects.get(name='Students')
            Notifications.objects.create(message=f"{course.name} / {topic.name} : New content has been added!",receivers=group,year=course.year) 
            
            return redirect('topic',course=course.name,topic=topic.name)
    context= {'form':form,'title':title}
    return render(request,'form.html',context) 
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def ContentDelete(request,topic,name,id): 
    topic    = CourseTopic.objects.get(name=topic)    
    content  = Content.objects.get(id=id,topic=topic,name=name)
    print(content)
    content.delete()
    return redirect('topic',course=topic.course,topic=topic)


@login_required(login_url='login')
def Assignment(request,course,topic,assignment):
    from datetime import date
    topic    = CourseTopic.objects.get(name=topic)
    course   = Courses.objects.get(name=course)
    if request.user.is_teacher:
        if Teachers.objects.get(user =request.user).course == course:
            
            teacher_course = True
        else:
            teacher_course = False  
    else:
        teacher_course = False 
    assignment = ClassWork.objects.get(title=assignment)
    deadline   = date.today()
    
    if request.user.is_student:
        if StudentWorks.objects.filter(assignment=assignment,student=Students.objects.get(user =request.user)).all():
            worked_already_sub = True
        else:
            worked_already_sub = False  
    else:
            worked_already_sub = False         
        
    if request.method == 'POST':
        file = request.FILES['file']
        StudentWorks.objects.create(
            topic      = topic,
            course     = course,
            assignment = assignment,
            student    = Students.objects.get(user=request.user),
            file       = file, 
        )        
        return redirect('topic',course = course.name,topic = topic.name)
    context = {'assignment':assignment,'deadline':deadline,'worked_already_sub':worked_already_sub,'teacher_course':teacher_course}  
    return render(request,'assignment.html',context)    
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def AssignmentAddForm(request,course,topic):
    topic    = CourseTopic.objects.get(name=topic)
    course   = Courses.objects.get(name=course)
    form  = AssignmentForm()
    title = 'Add Assignment'
    if request.method == 'POST':
        form = AssignmentForm(request.POST,request.FILES) 
        if form.is_valid():
            ClassWork.objects.create(
            topic  = topic,
            course = course,
            year   = course.year, 
            author = Teachers.objects.get(user=request.user),
            deadline = request.POST['deadline'],
            instructions = request.POST['instructions'],
            title = request.POST['title'],
            file = request.FILES['file'],
            )
            
            group  = Group.objects.get(name='Students')
            Notifications.objects.create(message=f"{course.name} / {topic.name}: New assignment has been added!",receivers=group,year=course.year) 
            return redirect('topic',course = course.name,topic = topic.name)

    context = {'form':form,'title':title} 
    return render (request,'form.html',context)       


@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def StudentWorkList(request,course,topic,assignment):
    
    topic       = CourseTopic.objects.get(name=topic)
    course      = Courses.objects.get(name=course)
    assignment  = ClassWork.objects.get(title=assignment)        
    works       = StudentWorks.objects.filter(assignment =assignment).all()
    students    = Students.objects.filter(year=course.year).all()
    

    total_works = 0
    for w in works:
        total_works += 1
    total_students = 0 
    for s in students:
        total_students += 1 
    context = {'assignment':assignment,'works':works,'total_works':total_works,'total_students':total_students,}      
    return render(request,'students_works_list.html',context)      
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def StudentWork(request,course,topic,assignment,work_id):
    assignment = ClassWork.objects.get(title=assignment)
    work       = StudentWorks.objects.get(id=work_id)
    form       = WorkReviewForm(instance=work)
    print(work.student.email)
    if request.method == 'POST':
        form       = WorkReviewForm(request.POST,instance=work) 
        if form.is_valid():
            grade = request.POST['grade'] 
            if int(grade) >= 6:
                form.instance.status = 'Passed'
            else:
                form.instance.status = 'Failed'
            form.save()
            receiver = UserAccount.objects.get(email = work.student.email)
            Notifications.objects.create(message=f"{topic} / {assignment.title} : Your homework has been reviewed!",unique_receiver=receiver)
            return redirect('student_works', course=work.course.name, topic=work.topic.name, assignment=work.assignment)
    context = {'assignment':assignment,'work':work,'form':form}
    return render(request,'assignment_form.html',context)         


@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def YearsViews(request):
    data = user_profile(request)
    user = data['user']
    years = SchoolYears.objects.all()    
    title    = 'SchoolYears'     
    create_url   =  'year_create'     
    context  = {'years':years,'title':title,'user':user,'create_url':create_url}
    return render(request,'request_list.html',context)  
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins'])
def YearData(request,pk):
    year = SchoolYears.objects.get(id=pk)
    students  = Students.objects.filter(year = year)
    courses   = Courses.objects.filter(year = year)
    
    
    context   = {'year':year,'students':students,'courses':courses}
    return render(request,'year_data.html',context)  


@login_required(login_url='login')
def EventsView(request):
    data = user_profile(request)
    user    = data['user']   
    events  = data['events']  
    filters = EventsFilters(request.GET,queryset=events)
    events  = filters.qs
    title   = 'Events'
    request_data = 'event'
    create_url = 'event_create'
    context = {'user':user,'events':events,'filters':filters,'title':title,'request_data':request_data,'create_url':create_url}
    return render(request,'request_list.html',context)
@login_required(login_url='login')
def EventData(request,title,date):
    event = Events.objects.get(title=title,event_date=date)
    comments = Comments.objects.filter(event=event).order_by('-date_added').all()
    total_comments = 0
    for comment in comments:
        total_comments += 1
    context = {'event':event,'comments':comments,'total_comments':total_comments}
    return render(request,'event_data.html',context)
@login_required(login_url='login')
@allowed_user(allowed_roles=['Admins','Teachers'])
def EventCreate(request):
    form = EventForm()
    title = 'Add Event'
    if request.method == 'POST':
        form = EventForm(request.POST,)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            year = SchoolYears.objects.get(id=request.POST['year'])
            group  = Group.objects.get(name='Students')
            Notifications.objects.create(message=f"New event added!",receivers=group,year=year) 
            messages.success(request,'Event successfully added')
            return redirect('events')
    context={'form':form,'title':title}
    return render(request,'form.html',context)

@login_required(login_url='login')
def CommentAdd(request,pk):
    event = Events.objects.get(id=pk)
    if request.method == 'POST':
        message = request.POST['message']
        Comments.objects.create(
            event        = event,
            user         = request.user,
            menssage     = message         
        )
    return redirect('event',title=event.title, date=event.event_date)
@login_required(login_url='login')
def CommentDelete(request,pk):
    comment = Comments.objects.get(id=pk)    
    comment.delete()
    event     = Events.objects.get(id=comment.event.id)
    return redirect('event',title=event.title, date=event.event_date)


