from django.db import models
from django.contrib.auth.models import  *
from django_countries.fields import CountryField
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import date
import datetime






def location_students(instance,filename):
    return f"users/students/{instance.full_name}/{filename}"

def location_teachers(instance,filename):
    return f"users/teachers/{instance.full_name}/{filename}"    

class UserManager(BaseUserManager):

    def create_user(self,email,password=None,**extra_field):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(email=self.normalize_email(email),**extra_field)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self,email,password):
        user = self.create_user(email,password)        
        user.is_superuser = True 
        user.is_staff = True
        user.save(using=self._db)
        return user   
                 
class UserAccount(AbstractBaseUser,PermissionsMixin):
    
    email           = models.EmailField(unique=True)        
    groups          = models.ManyToManyField(Group,blank=True)     
    date_joined     = models.DateTimeField(auto_now_add=timezone.now())
    last_login      = models.DateTimeField(auto_now=timezone.now())    
    is_active       = models.BooleanField(default=True)    
    is_superuser    = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False) 
   
    objects = UserManager()
    USERNAME_FIELD  = 'email'

    def __str__(self):
        return self.email




class Account(models.Model):
    id              = models.AutoField(primary_key=True) 
    user            = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200)
    date_of_birth   = models.DateField(default=datetime.date.today)
    gender_choice   = (('male','male'),('feminine','feminine'),('undefined','undefined'))  
    gender          = models.CharField(max_length=10, default='male', choices=gender_choice)
    nationality     = CountryField()

    class Meta:
        abstract = True


class Students(Account):
    year            = models.ForeignKey(to='main_app.SchoolYears',on_delete=models.CASCADE,blank=True,null=True)
     
    

    class Meta():
        verbose_name        = 'Student'
        verbose_name_plural = 'Students'

    def get_absolute_url(self):
        return f"academiaweb/students/{self.id}"    

    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)    
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


class Teachers(Account):

    course          = models.ForeignKey(to='main_app.Courses',on_delete=models.DO_NOTHING,null=True,blank=True)    
    profile_picture = models.ImageField(blank=True,null=True, upload_to=location_teachers)
    
    class Meta():
        verbose_name        = 'Teacher'
        verbose_name_plural = 'Teachers'

    def get_absolute_url(self):
        return f"academiaweb/teachers/{self.id}"       
    
    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)

    @property
    def email(self):
        return str(self.user)
        
    def teacher_course(self):
        return str(self.course)

    def delete(self,*args,**kwargs):
        self.profile_picture.delete()
        super().delete(*args,**kwargs)    