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

class ApplicationsForm(forms.ModelForm):
    # phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    class Meta:
        model = Applications
        fields = '__all__'
        widgets={
        'date_of_birth' : DateInput(),        
        }

class  StudentsForm(forms.ModelForm):
    class Meta:
        model   = Students
        exclude = ('user',)  

class  TeachersForm(forms.ModelForm):
    class Meta:
        model   = Teachers
        exclude = ('user',)

class  AdminsForm(forms.ModelForm):
    class Meta:
        model   = Admins
        exclude = ('user',)        

class  CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'

class  CategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        exclude = ('course','year')

class  ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        exclude = ('category',)