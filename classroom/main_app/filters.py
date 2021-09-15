from django.contrib.auth.models import User
from django.forms.widgets import TextInput,SelectMultiple 
from django import forms
from django_filters import DateFilter
import django_filters
from .models import *

class ApplyFilters(django_filters.FilterSet):
    class Meta:
        model   = Applications
        exclude = ('sent_date','profile_picture','HS_diploma','date_of_birth','nationality')

class StudentsFilters(django_filters.FilterSet):
    class Meta:
        model   = Students
        exclude = ('sent_date','profile_picture','HS_diploma','date_of_birth','nationality')

class TeachersFilters(django_filters.FilterSet):
    class Meta:
        model   = Teachers        
        exclude = ('description','sent_date','profile_picture','HS_diploma','date_of_birth','nationality','user')

class CoursesFilters(django_filters.FilterSet):
    class Meta:
        model   =  Courses
        exclude = ('course_picture','description')