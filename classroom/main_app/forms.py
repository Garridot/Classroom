from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class  CoursesForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'

class  TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
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
        model   = School_Assignment
        exclude = ('author','course','topic','year')   
        widgets={
        'deadline' : DateInput(),        
        }     
class ReviewForm(forms.ModelForm): 
    class Meta:
        model   = Students_Assignment
        exclude = ('student','course','topic','assignment','status')
        labels  = {
            'comment' : 'Add a Comment(no required)'
        } 
