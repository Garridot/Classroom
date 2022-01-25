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

 