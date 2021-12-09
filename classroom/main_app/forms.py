from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import *

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget 
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(UserCreationForm):    
    class Meta:               
        model  = UserAccount
        exclude = ('password','user_permissions','groups','is_active','is_staff','is_superuser','is_teacher','is_student','is_admin')

class UpdateUserForm(forms.ModelForm):    
    class Meta:               
        model  = UserAccount
        exclude = ('password','password1','password2','user_permissions','groups','is_active','is_staff','is_superuser','is_teacher','is_student','is_admin')


class  StudentsForm(forms.ModelForm):
    class Meta:
        model   = Students
        exclude = ('user',)  
        widgets={
        'date_of_birth' : DateInput(),        
        }

class  TeachersForm(forms.ModelForm):
    class Meta:
        model   = Teachers
        exclude = ('user',)
        widgets={
        'date_of_birth' : DateInput(),        
        }

class  AdminsForm(forms.ModelForm):
    class Meta:
        model   = Admins
        exclude = ('user',)        

class  CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'

class  TopicForm(forms.ModelForm):
    class Meta:
        model = CourseTopic
        exclude = ('course','year')

class  ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        exclude = ('topic',)

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        exclude = ('author',)  
        widgets={
        'event_date' : DateInput(),        
        } 
class AssignmentForm(forms.ModelForm): 
    class Meta:
        model   = ClassWork
        exclude = ('author','course','topic','year')   
        widgets={
        'deadline' : DateInput(),        
        }     
class WorkReviewForm(forms.ModelForm): 
    class Meta:
        model   = StudentWorks
        exclude = ('student','course','topic','assignment','status','file')
        labels  = {
            'comment' : 'Add a Comment(no required)'
        } 
