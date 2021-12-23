from django.contrib.auth.models import User
from django.forms.widgets import TextInput,SelectMultiple 
from django import forms
from django_filters import DateFilter
import django_filters

from users.models import *
from .models import *





class CoursesFilters(django_filters.FilterSet):
    class Meta:
        model   =  Courses
        exclude = ('description')

class EventsFilters(django_filters.FilterSet):
    class Meta:
        model   =  Events
        exclude = ('message','author','created')

class TeachersFilters(django_filters.FilterSet):
    class Meta:
        model   =  Teachers
        exclude = ('user','profile_picture','date_of_birth','gender','nationality')        

class StudentsFilters(django_filters.FilterSet):
    class Meta:
        model   =  Students
        exclude = ('user','profile_picture','date_of_birth','gender','nationality')  