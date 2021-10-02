from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.deletion import CASCADE
from django_countries.fields import CountryField
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import date

# from phonenumber_field.modelfields import PhoneNumberField

import datetime 

# Create your models here.

class UserManager(BaseUserManager):

    def create_superuser(self,email,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        email = self.normalize_email(email)        
        return self.create_user(email, password, **other_fields)



    def create_user(self,email,password,**other_fields):  

        other_fields.setdefault('is_active',True)
        email = self.normalize_email(email)
        return self.create_user(email, password, **other_fields)
class UserAccount(AbstractBaseUser,PermissionsMixin):
    
    email           = models.EmailField(unique=True)        
    groups          = models.ManyToManyField(Group,blank=True)     
    date_joined     = models.DateTimeField(auto_now_add=timezone.now())
    last_login      = models.DateTimeField(auto_now=timezone.now())    
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_teacher      = models.BooleanField(default=False)
    is_student      = models.BooleanField(default=False)      
    is_admin        = models.BooleanField(default=False)  

    USERNAME_FIELD  = 'email'
   
    objects = UserManager()

    def __str__(self):
        return self.email


class SchoolYears(models.Model):

    id   = models.AutoField(primary_key=True)
    year = models.IntegerField()
    def __str__(self):
        return str(self.id)

    def year_id(self):
        return str(self.year)
    @property
    def total_students(self):
        students = 0
        get_students = self.students_set.all()

        for student in get_students:
            students += 1            
        return students

def upload_location_admins(instance,filename):
    return f"accounts/admins/{instance.full_name}/{filename}"
class Admins(models.Model):
    id              = models.AutoField(primary_key=True)    
    user            = models.ForeignKey(UserAccount,on_delete=models.CASCADE)       
    document        = models.CharField(max_length=8,unique=True) 
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200)
    # phone           = PhoneNumberField()    
    date_of_birth   = models.DateField(default=datetime.date.today) 
    gender_choice   = (('male','male'),('feminine','feminine'),('undefined','undefined'))  
    gender          = models.CharField(max_length=10, default='male', choices=gender_choice) 
    nationality     = CountryField()      
    description     = models.TextField(max_length=500,blank=True)
    profile_picture = models.ImageField(blank=True,null=True, upload_to=upload_location_admins)
    
    class Meta():
        verbose_name        = 'Admin'
        verbose_name_plural = 'Admins'
    
    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)
    @property
    def full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)
    @property
    def email(self):
        return str(self.user)

    def delete(self,*args,**kwargs):
        self.profile_picture.delete()
        super().delete(*args,**kwargs)          

def upload_location(instance,filename):
    return f'course/{instance.name}/course_picture/{filename}'         
class Courses(models.Model): 
    id             = models.AutoField(primary_key=True)
    name           = models.CharField(max_length=200)
    description    = models.TextField()
    year           = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)    
    course_picture = models.ImageField(blank=True,null=True, upload_to=upload_location) 

    class Meta():        
        verbose_name        = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name

    def delete(self,*args,**kwargs):
        self.course_picture.delete()
        super().delete(*args,**kwargs)      
  
class CourseTopic(models.Model):

    id          = models.AutoField(primary_key=True)    
    course      = models.ForeignKey(Courses,on_delete=models.CASCADE,)
    name        = models.CharField(max_length=200)
    description = models.TextField()   
    year        = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)

    class Meta():
        verbose_name        = 'Course Content'
        verbose_name_plural = 'Courses Content'


    def __str__(self):
        return self.name 

def upload_location_students(instance,filename):
    return f"accounts/students/{instance.full_name}/{filename}"
class Students(models.Model):

    id              = models.AutoField(primary_key=True) 
    user            = models.ForeignKey(UserAccount,on_delete=models.CASCADE)    
    document        = models.CharField(max_length=8,unique=True)    
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200)
    date_of_birth   = models.DateField(default=datetime.date.today)
    gender_choice   = (('male','male'),('feminine','feminine'),('undefined','undefined'))  
    gender          = models.CharField(max_length=10, default='male', choices=gender_choice)
    nationality     = CountryField() 
    # phone           = PhoneNumberField()
    year            = models.ForeignKey(SchoolYears,on_delete=models.CASCADE,blank=True,null=True)
    profile_picture = models.ImageField(upload_to=upload_location_students,blank=True,null=True)    
    HS_diploma      = models.FileField(upload_to=upload_location_students,blank=True,null=True)

    class Meta():
        verbose_name        = 'Student'
        verbose_name_plural = 'Students'
    @property
    def full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)
    @property
    def email(self):
        return str(self.user)
    @property
    def age(self):
        age = date.today().year - self.date_of_birth.year
        return age 

    def delete(self,*args,**kwargs):
        self.profile_picture.delete()
        self.HS_diploma.delete()
        super().delete(*args,**kwargs)             

def upload_location_teachers(instance,filename):
    return f"accounts/teachers/{instance.full_name}/{filename}"
class Teachers(models.Model):

    id              = models.AutoField(primary_key=True)    
    user            = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    courses         = models.ForeignKey(Courses,on_delete=models.DO_NOTHING,null=True,blank=True)      
    document        = models.CharField(max_length=8,unique=True) 
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200)    
    date_of_birth   = models.DateField(default=datetime.date.today) 
    gender_choice   = (('male','male'),('feminine','feminine'),('undefined','undefined'))  
    gender          = models.CharField(max_length=10, default='male', choices=gender_choice) 
    nationality     = CountryField()         
    description     = models.TextField(max_length=500,blank=True)
    profile_picture = models.ImageField(blank=True,null=True, upload_to=upload_location_teachers)
    
    class Meta():
        verbose_name        = 'Teacher'
        verbose_name_plural = 'Teachers'
    
    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)

    @property
    def email(self):
        return str(self.user)
        
    def course(self):
        return str(self.courses)

    def delete(self,*args,**kwargs):
        self.profile_picture.delete()
        super().delete(*args,**kwargs)    

class Notifications(models.Model):

    id       = models.AutoField(primary_key=True)
    sender   = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='sender') 
    message  = models.CharField(max_length=100)
    receiver = models.ForeignKey(UserAccount,null=True,blank=True,on_delete=models.DO_NOTHING,related_name='receiver')
    link     = models.URLField(null=True,blank=True)   
    year     = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)
    created  = models.DateTimeField(auto_now_add=True)  
    unread   = models.BooleanField(default=True) 
    def __str__(self):
        return str(self.message)

def upload_location_content(instance,filename):
    return f'course/{instance.topic.course}/{instance.topic}/files/{filename}'       
class Content(models.Model): 
    id       = models.AutoField(primary_key=True)    
    topic    = models.ForeignKey(CourseTopic,on_delete=models.CASCADE)
    name     = models.CharField(max_length=50)        
    field    = models.FileField(upload_to=upload_location_content)
    created  = models.DateTimeField(auto_now_add=timezone.now())
    class Meta():
        verbose_name        = 'Content'
        verbose_name_plural = 'Contents'
        
    def __str__(self):
        return str(self.field)

    def delete(self,*args,**kwargs):
        self.field.delete()
        super().delete(*args,**kwargs)


class Applications(models.Model):

    id              = models.AutoField(primary_key=True)
    email           = models.EmailField()    
    document        = models.CharField(max_length=8) 
    nationality     = CountryField()
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200,)    
    date_of_birth   = models.DateField()
    gender_choice   = (('male','male'),('feminine','feminine'),('undefined','undefined'))  
    gender          = models.CharField(max_length=10, default='male', choices=gender_choice)   
    year            = models.ForeignKey(SchoolYears,on_delete=models.DO_NOTHING)    
    sent_date       = models.DateTimeField(auto_now_add=True,)    
    profile_picture = models.ImageField(upload_to=upload_location_students,blank=True,null=True)
    HS_diploma      = models.FileField(upload_to=upload_location_students,blank=True,null=True,)
      
    @property
    def full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)

    def delete(self,*args,**kwargs):
        self.profile_picture.delete()
        self.HS_diploma.delete()
        super().delete(*args,**kwargs)      

class Events(models.Model):
    id          = models.AutoField(primary_key=True)  
    title       = models.CharField(max_length=50)
    message     = models.TextField()
    event_date  = models.DateField()    
    year        = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)
    author      = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    created     = models.DateTimeField(auto_now_add=datetime.datetime.now())
    class Meta():
        verbose_name        = 'Event'
        verbose_name_plural = 'Events'

class Comments(models.Model):
    event        = models.ForeignKey(Events,on_delete=models.CASCADE, related_name='comments')   
    user         = models.ForeignKey(UserAccount,on_delete=models.CASCADE) 
    menssage     = models.TextField()
    date_added   = models.DateTimeField(auto_now_add=True)
    
class History(models.Model):
    student     = models.ForeignKey(Students,on_delete=models.CASCADE)
    content_id  = models.ForeignKey(Content,on_delete=models.CASCADE)
    topic_id    = models.ForeignKey(CourseTopic,on_delete=models.CASCADE)
    course_id   = models.ForeignKey(Courses,on_delete=models.CASCADE)
    seen        = models.DateTimeField(auto_now_add=timezone.now())



def upload_location_assignment(instance,filename):
    return  f'course/{instance.course}/{instance.topic}/assignment/{filename}'
class ClassWork(models.Model):
    author   = models.ForeignKey(Teachers,on_delete=models.CASCADE)
    year     = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)
    course   = models.ForeignKey(Courses,on_delete=models.CASCADE)
    topic    = models.ForeignKey(CourseTopic,on_delete=models.CASCADE)
    title    = models.CharField(max_length=50) 
    instructions = models.TextField()
    file     = models.FileField(upload_to=upload_location_assignment,null=True,blank=True)
    deadline = models.DateField(null=True,blank=True)
    created = models.DateTimeField(auto_now=datetime.datetime.now())

    def __str__(self):
        return self.title

    def delete(self,*args,**kwargs):
        self.file.delete()
        super().delete(*args,**kwargs)    


def upload_location_studentwork(instance,filename):
    return  f'course/{instance.course}/{instance.topic}/assignment/studentworks/{filename}'    
class StudentWorks(models.Model):
    assignment = models.ForeignKey(ClassWork,on_delete=models.CASCADE)
    student   = models.ForeignKey(Students,on_delete=models.CASCADE)
    course    = models.ForeignKey(Courses,on_delete=models.CASCADE)
    topic     = models.ForeignKey(CourseTopic,on_delete=models.CASCADE)
    file      = models.FileField(upload_to=upload_location_studentwork,null=True,blank=True)
    comment   = models.TextField(null=True,blank=True)
    grade     = models.PositiveIntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)],null=True,blank=True)
    status_choice   = (('Passed','Passed'),('Unchecked','Unchecked'),('Failed','Failed'))  
    status    = models.CharField(max_length=10, default='Unchecked', choices=status_choice,null=True,blank=True)
    
    def __str__(self):
        return f"{self.assignment.title}"

    