from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'
class UserForm(UserCreationForm):    
    class Meta:               
        model  = UserAccount
        exclude = ('password','user_permissions','groups','is_active','is_staff','is_superuser',)

class UserAccountForm(forms.ModelForm):    
    class Meta:               
        model  = UserAccount
        exclude = ('password','password1','password2','user_permissions','groups','is_active','is_staff','is_superuser',)


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