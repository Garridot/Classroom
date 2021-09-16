from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser,PermissionsMixin
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
    profile_picture = models.ImageField(blank=True,null=True, upload_to='admins/profile_pictures')
    
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
        
class Courses(models.Model):   

    id             = models.AutoField(primary_key=True)
    name           = models.CharField(max_length=200)
    description    = models.TextField()
    year           = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)    
    course_picture = models.ImageField(blank=True,null=True, upload_to='course_pictures') 

    class Meta():        
        verbose_name        = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name
   
class CourseCategory(models.Model):

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
    profile_picture = models.ImageField(upload_to='students/profile_pictures',blank=True,null=True)    
    HS_diploma      = models.FileField(upload_to='students/high_school_diploma',blank=True,null=True)

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

class Teachers(models.Model):

    id              = models.AutoField(primary_key=True)    
    user            = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    courses         = models.ForeignKey(Courses,on_delete=models.CASCADE)      
    document        = models.CharField(max_length=8,unique=True) 
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200)    
    date_of_birth   = models.DateField(default=datetime.date.today) 
    gender_choice   = (('male','male'),('feminine','feminine'),('undefined','undefined'))  
    gender          = models.CharField(max_length=10, default='male', choices=gender_choice) 
    nationality     = CountryField()         
    description     = models.TextField(max_length=500,blank=True)
    profile_picture = models.ImageField(blank=True,null=True, upload_to='teachers/profile_pictures')
    
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

class Notifications(models.Model):

    id       = models.AutoField(primary_key=True)
    user     = models.ForeignKey(UserAccount,on_delete=CASCADE) 
    message  = models.CharField(max_length=100)
    link     = models.URLField(null=True,blank=True)   
    year     = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)
    created  = models.DateTimeField(auto_now_add=True)  
    unread   = models.BooleanField(default=True) 
    def __str__(self):
        return str(self.message)
      
class Content(models.Model): 

    id       = models.AutoField(primary_key=True)    
    category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    name     = models.CharField(max_length=50)        
    field    = models.FileField(upload_to='pdf')
    created  = models.DateTimeField(auto_now_add=timezone.now())
    class Meta():
        verbose_name        = 'Content'
        verbose_name_plural = 'Contents'
        
    @property
    def name_unit(self):
        
        return str(self.unit)

    def __str__(self):
        return str(self.field)

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
    # phone           = PhoneNumberField()
    year            = models.ForeignKey(SchoolYears,on_delete=models.DO_NOTHING)    
    sent_date       = models.DateTimeField(auto_now_add=True,)    
    profile_picture = models.ImageField(upload_to='applications/profile_pictures',blank=True,null=True)
    HS_diploma      = models.FileField(upload_to='applications/high_school_diploma',blank=True,null=True,)
      
    @property
    def full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)

class Events(models.Model):
    id          = models.AutoField(primary_key=True)  
    title       = models.CharField(max_length=50)
    message     = models.TextField()
    event_date  = models.DateField()
    course      = models.ForeignKey(Courses,on_delete=models.CASCADE)
    year        = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)
    author      = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    created     = models.DateTimeField(auto_now_add=datetime.datetime.now())
    class Meta():
        verbose_name        = 'Event'
        verbose_name_plural = 'Events'

class Comments(models.Model):
    event       = models.ForeignKey(Events,on_delete=models.CASCADE, related_name='comments')   
    user         = models.ForeignKey(UserAccount,on_delete=models.CASCADE) 
    menssage     = models.TextField()
    date_added   = models.DateTimeField(auto_now_add=True)
    reply        = models.ForeignKey('self',on_delete=models.CASCADE, blank=True, null=True) 
    
    @property
    def replies(self):
        return Comments.objects.filter(reply='self').order_by('-date_added').all()
