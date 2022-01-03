from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import datetime 



# Create your models here.

def upload_location_content(instance,filename):
    return f'course/{instance.topic.course}/{instance.topic}/files/{filename}'   

def location_assignment(instance,filename):
    return  f'course/{instance.topic.course}/{instance.topic}/{instance.title}/{filename}'

def location_students_assignment(instance,filename):
    return  f'course/{instance.assignment.topic.course}/{instance.assignment.topic}/{instance.assignment}/students_assignment/{filename}'



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
       
class Courses(models.Model): 
    id             = models.AutoField(primary_key=True)
    name           = models.CharField(max_length=200)
    description    = models.TextField()
    year           = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)    
    

    class Meta():        
        verbose_name        = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name

          
  
class Topic(models.Model):

    id          = models.AutoField(primary_key=True)    
    course      = models.ForeignKey(Courses,on_delete=models.CASCADE,)
    name        = models.CharField(max_length=200)
    description = models.TextField()   
    

    class Meta():
        verbose_name        = 'Course Content'
        verbose_name_plural = 'Courses Content'


    def __str__(self):
        return self.name 

    
class Content(models.Model): 
    id       = models.AutoField(primary_key=True)    
    topic    = models.ForeignKey(Topic,on_delete=models.CASCADE)
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

class Events(models.Model):
    id          = models.AutoField(primary_key=True)  
    title       = models.CharField(max_length=50)
    message     = models.TextField()
    event_date  = models.DateField()    
    year        = models.ForeignKey(SchoolYears,on_delete=models.CASCADE)    
    created     = models.DateTimeField(auto_now_add=datetime.datetime.now())
    class Meta():
        verbose_name        = 'Event'
        verbose_name_plural = 'Events'

    def get_absolute_url(self):
        return f"http://127.0.0.1:8000/academiaweb/events/{self.id}"

class Comments(models.Model):
    event        = models.ForeignKey(Events,on_delete=models.CASCADE, related_name='comments')   
    user         = models.ForeignKey(to='users.UserAccount',on_delete=models.CASCADE) 
    menssage     = models.TextField()
    date_added   = models.DateTimeField(auto_now_add=True)
    
class History(models.Model):
    student     = models.ForeignKey(to='users.Students',on_delete=models.CASCADE)
    content_id  = models.ForeignKey(Content,on_delete=models.CASCADE)
    topic_id    = models.ForeignKey(Topic,on_delete=models.CASCADE)
    course_id   = models.ForeignKey(Courses,on_delete=models.CASCADE)
    seen        = models.DateTimeField(auto_now_add=timezone.now())

    def __str__(self):
        return f"{self.content_id.name}"

class School_Assignment(models.Model):
    topic    = models.ForeignKey(Topic,on_delete=models.CASCADE)
    title    = models.CharField(max_length=50) 
    instructions = models.TextField()
    file     = models.FileField(upload_to=location_assignment,null=True,blank=True)
    deadline = models.DateField(null=True,blank=True)
    created  = models.DateTimeField(auto_now=datetime.datetime.now())

    def __str__(self):
        return self.title

    def delete(self,*args,**kwargs):
        self.file.delete()
        super().delete(*args,**kwargs)

    def get_absolute_url(self):        
        return f"academiaweb/courses/{self.topic.course.id}/topic/{self.topic.id}/assignments/{self.id}"     
    
    
class Students_Assignment(models.Model):
    assignment = models.ForeignKey(School_Assignment,on_delete=models.CASCADE)    
    student    = models.ForeignKey(to='users.Students',on_delete=models.CASCADE)       
    file       = models.FileField(upload_to=location_students_assignment,null=True,blank=True)    
    grade      = models.PositiveIntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)],null=True,blank=True)
    status_choice   = (('Passed','Passed'),('Unchecked','Unchecked'),('Failed','Failed'))  
    status    = models.CharField(max_length=10, default='Unchecked', choices=status_choice,null=True,blank=True)
    
    def __str__(self):
        return f"{self.assignment.title}"

    def get_absolute_url(self):        
        return f"academiaweb/courses/{self.assignment.topic.course.id}/topic/{self.assignment.topic.id}/assignments/{self.assignment.id}/students_assignment/{self.id}"             

    