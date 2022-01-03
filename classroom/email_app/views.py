from django.shortcuts import render
from main_app.models import SchoolYears
from main_app.models import Courses
from main_app.models import Students_Assignment, Topic
from main_app.models import Events
from classroom.settings  import  EMAIL_HOST_USER
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.models import *
from django.core.mail import send_mail
# Create your views here.

def PasswordResetEmail(user): 
    
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

def RegisterEMAIL(email):
    user = UserAccount.objects.get(email=email)  
    context   = {'email':email,'user':user}     
    template  = get_template('users/emails/register_email.html')
    content   = template.render(context)

    email     = EmailMultiAlternatives(
        f'Congratulations {user.email}!',
        'Your register has been successfully accepted.',
        EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(content,'text/html')
    email.send()

def EventEmail(title,year):
    year = SchoolYears.objects.get(id=year)

    students = Students.objects.filter(year=year).all()  
    
    event  = Events.objects.filter(title=title,year=year).last()

    

    
    
    for student in students:   
        subject = f'New event: {title}'
        message = f"Hi {student.full_name}, a new event has been published.\nLink: {event.get_absolute_url}"
        
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [student.user.email]
        )

def TopicEmail(id):
    course   = Courses.objects.get(id=id)
    url = f"http://127.0.0.1:8000/academiaweb/courses/{course.id}/" 
    
    students = Students.objects.filter(year=course.year).all()       
    for student in students:   
        subject = f'New Topic: {course.name}'
        message = f"Hi {student.full_name}, a new topic has been published.\nLink: {url}"
        
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [student.user.email]
        )        

def Contentemail(id):
    topic = Topic.objects.get(id=id)
    url = f"http://127.0.0.1:8000/academiaweb/courses/{topic.course.id}/topics/{topic.id}/" 

    students = Students.objects.filter(year=topic.course.year).all()    
    for student in students:   
        subject = f'New Content: {topic.name}'
        message = f"Hi {student.full_name}, a new content has been published.\nLink: {url}"
        
        
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [student.user.email]
        )        

def Homeworkemail(id):
    homework=Students_Assignment.objects.get(id=id)  
    student = Students.objects.get(id=homework.student.id) 
    url  = 'http://127.0.0.1:8000/academiaweb/grades'
    subject = f'Homework: {homework.assignment}'
    message = f"Hi {student.full_name}, your homework has been review.\nLink: {url}"
    
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [student.user.email]
    )            