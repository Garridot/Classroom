from classroom.settings  import  EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django_filters.views import FilterView
from django.utils import timezone 
from .models import * 
from .forms import *
from .utils import *
from .filters import*
from .decorators import *
from users.models import *
from users.forms import *
import json

from email_app.views import *

# django_q
from django_q.tasks import async_task



# Create your views here.

def MainPage(request):
    return render(request,'main_page.html')
def Information(request):
    return render(request,'information.html')
def Contact(request):    
    if request.method == 'POST':
        name    = request.POST['name']
        email   = request.POST['email']
        message = request.POST['message']
        send_mail(
            'Message from' + name,
            message,
            email,
            [EMAIL_HOST_USER],
        )
        return render(request,'contact.html',{'name':name}) 
    return render(request,'contact.html',{}) 


@login_required(login_url='login')
def HomeView(request):    

    calendar = GetCalendar.calendar()   
    events   = Events.objects.filter(event_date__month=timezone.now().month).all() 
    
    list1        = UserObjs.request_user(request.user)['list1']
    list2        = UserObjs.request_user(request.user)['list2']
    user_request = UserObjs.request_user(request.user)['user_request']

    
    context = {
                
                'calendar' : calendar,
                'events'   : events,
                'user_request':user_request,
                'list1'    : list1,
                'list2'    : list2            
    }
    return render(request,'home.html',context) 



def HistoryView(request):    
    data = json.load(request)['content']        
    if request.user.groups.all()[0].name == 'Students':    

        student = Students.objects.get(user=request.user)
        content = Content.objects.get(id=data)
        try:
            hitorial  = History.objects.get(student=student,content_id=content)
            if hitorial:
                History.objects.filter(student=student,content_id=content).update(seen=timezone.now())
        except:              
            History.objects.create(student=student,content_id=content,topic_id=content.topic,course_id=content.topic.course)

    return None        


class LoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    

#  Courses

class CoursesList(FilterView):
    model            = Courses
    filterset_class  = CoursesFilters
    template_name    = 'courses/courses_list.html' 

    

class CourseCreate(CreateView):
    model  = Courses
    form_class = CoursesForm    
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses')

    def form_valid(self,form):
        messages.success(self.request, f"Course created successfully")
        return super().form_valid(form) 

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)               
        context['title']       = 'Create Course'
        return context     

class CourseData(DetailView):
    model         = Courses
    template_name = 'courses/course_object.html'
    
    def get_object(self):
        pk_ = self.kwargs.get('course_pk')
        return get_object_or_404(Courses,id=pk_)

    def get_context_data(self, **kwargs):   
        pk_ = self.kwargs.get('course_pk')     
        context = super().get_context_data(**kwargs)        
        context['topics'] = Topic.objects.filter(course=pk_)
        return context    

class CourseUpdate(UpdateView):
    model = Courses
    form_class = CoursesForm
    success_url = reverse_lazy('courses')
    template_name = 'courses/course_form.html' 

    def get_object(self):
        pk_ = self.kwargs.get('course_pk')
        return get_object_or_404(Courses,id=pk_)

    def form_valid(self,form):
        messages.success(self.request, f"Course updated successfully")
        return super().form_valid(form) 

    def get_success_url(self):
        return reverse_lazy('course_data',kwargs={'course_pk':CourseUpdate.get_object(self).id})

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)               
        context['title']       = 'Update Course'
        return context      

class CourseDelete(DeleteView):
    model = Courses  

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)    

    def get_object(self):
        pk_ = self.kwargs.get('course_pk')
        return get_object_or_404(Courses,id=pk_)
      

    def get_success_url(self):
        messages.success(self.request, f"Course deleted successfully")
        return reverse_lazy('courses')   


# Topics

class TopicCreate(CreateView):

    model         = Topic
    form_class    = TopicForm    
    template_name = 'courses/course_form.html'     

    def get_object(self):              
        return  get_object_or_404(Courses,id=self.kwargs.get('course_pk'))

    def form_valid(self,form):
        form.instance.course = TopicCreate.get_object(self)
        form.instance.year   = TopicCreate.get_object(self).year               
        return super().form_valid(form) 


    def get_success_url(self):
        async_task('email_app.views.Contentemail',TopicCreate.get_object(self).id)
        messages.success(self.request, f"Topic created successfully")         
        return reverse_lazy('course_data', kwargs={'course_pk': TopicCreate.get_object(self).id }) 

    def get_context_data(self, **kwargs):   
        course  =  get_object_or_404(Courses,id=self.kwargs.get('course_pk')).id 
        context = super().get_context_data(**kwargs) 
        context['course']      = Courses.objects.get(id=course)        
        context['title']       = 'Create Topic'
        return context 

class TopicDetail(DetailView):

    model         = Topic
    template_name = 'courses/topics/topic_object.html'

    
    def get_object(self): 
        return get_object_or_404(Topic,id=self.kwargs.get('topic_pk')) 


    def get_context_data(self, **kwargs):   
        course  =  get_object_or_404(Courses,id=self.kwargs.get('course_pk')).id 
        topic   =  TopicDetail.get_object(self)

        context = super().get_context_data(**kwargs) 
        context['course']      = Courses.objects.get(id=course)
        context['contents']    = Content.objects.filter(topic=topic)       
        context['assignments'] = School_Assignment.objects.filter(topic=topic)
        
        return context

class TopicUpdate(UpdateView):

    model = Topic
    form_class = TopicForm    
    template_name = 'courses/course_form.html' 

    def get_object(self): 
        return get_object_or_404(Topic,id=self.kwargs.get('topic_pk'))   


    def form_valid(self,form):
        messages.success(self.request, f"Course updated successfully")
        return super().form_valid(form)   

    def get_success_url(self):
        course  =  get_object_or_404(Courses,id=self.kwargs.get('course_pk')).id 
        topic   =  TopicDetail.get_object(self).id
        return reverse_lazy('topic', kwargs={'course_pk': course ,'topic_pk' : topic}) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)               
        context['title']       = 'Update Topic'
        return context     

class TopicDelete(DeleteView):

    model = Topic

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)  

    def get_object(self):        
        return get_object_or_404(Topic,id=self.kwargs.get('topic_pk'))

    def get_success_url(self):
        course = get_object_or_404(Courses,id=self.kwargs.get('course_pk')).id
        messages.success(self.request, f"Topic deleted successfully")
        return reverse_lazy('course_data', kwargs={'course_pk': course})   


# Contents

class ContentCreate(CreateView):
    model         = Content
    form_class    = ContentForm    
    template_name = 'courses/course_form.html'

    def form_valid(self,form):

        topic = get_object_or_404(Topic,id=self.kwargs.get('topic_pk'))

        form.instance.topic = topic
        messages.success(self.request, f"Content added successfully") 
        async_task('email_app.views.Contentemail',topic.id)                      
        return super().form_valid(form)

    def get_success_url(self):

        course  =  get_object_or_404(Courses,id=self.kwargs.get('course_pk')).id 
        topic   =  get_object_or_404(Topic,id=self.kwargs.get('topic_pk')).id        
        return reverse_lazy('topic', kwargs={'course_pk': course ,'topic_pk' : topic}) 

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)               
        context['title']       = 'Add Content'
        return context        

class ContentDelete(DeleteView):
    model         = Content

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)  

    def get_object(self):        
        return get_object_or_404(Content,id=self.kwargs.get('content_pk'))

    def get_success_url(self):

        course = get_object_or_404(Courses,id=self.kwargs.get('course_pk')).id
        topic  = get_object_or_404(Topic,id=self.kwargs.get('topic_pk')).id
        messages.success(self.request, f"Content deleted successfully")
        return reverse_lazy('topic', kwargs={'course_pk': course,'topic_pk':topic}) 


# Students

class StudentsList(FilterView):
    model = Students
    filterset_class  = StudentsFilters
    template_name = 'users/students_list.html'

def StudentCreate(request):    
   
    form        = UserForm
    title       = 'Create Students'
    form_kwargs = StudentsForm

    if request.method == 'POST':
        form        = UserForm(request.POST)
        form_kwargs = StudentsForm(request.POST,request.FILES)        

        if form.is_valid() and form_kwargs.is_valid(): 
            Create_Student.create(form,form_kwargs)             
            messages.success(request,'Student created successfully.')
            return redirect('students_list')            
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 

    context = {'form':form,'form_kwargs':form_kwargs,'title':title}
    return render (request,'form.html',context)

class StudentData(DetailView):
    model         = Students
    template_name = 'users/user_object.html'
    
    def get_object(self):
        pk_ = self.kwargs.get('student_pk')
        return get_object_or_404(Students,id=pk_)

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs) 
        return context    

class StudentUpdate(UpdateView):
    model = Students
    form_class = StudentsForm
    success_url = reverse_lazy('students')
    template_name = 'courses/course_form.html' 

    def get_object(self):
        pk_ = self.kwargs.get('student_pk')
        return get_object_or_404(Students,id=pk_)

    def form_valid(self,form):
        messages.success(self.request, f"Student updated successfully")
        return super().form_valid(form) 

    def get_success_url(self):
        return reverse_lazy('student_data',kwargs={'student_pk':CourseUpdate.get_object(self).id})

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)               
        context['title']       = 'Update Student'
        return context      

class StudentDelete(DeleteView):
    model = UserAccount

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)  

    def get_object(self):        
        return get_object_or_404(UserAccount,id=self.kwargs.get('user_pk'))

    def get_success_url(self):        
        messages.success(self.request, f"Students deleted successfully")
        return reverse_lazy('students_list')


# Teachers

class TeachersList(FilterView):
    model            = Teachers
    filterset_class  = TeachersFilters
    template_name    = 'users/teacher_list.html'

def TeacherCreate(request):    
   
    form        = UserForm
    title       = 'Create Teacher'
    form_kwargs = TeachersForm

    if request.method == 'POST':
        form        = UserForm(request.POST)
        form_kwargs = TeachersForm(request.POST,request.FILES)        

        if form.is_valid() and form_kwargs.is_valid(): 
            Create_Teacher.create(form,form_kwargs)             
            messages.success(request,'Teacher created successfully.')
            return redirect('teachers_list')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 

    context = {'form':form,'form_kwargs':form_kwargs,'title':title}
    return render (request,'form.html',context) 

class TeacherData(DetailView):
    model         = Teachers
    template_name = 'users/user_object.html'
    
    def get_object(self):
        pk_ = self.kwargs.get('teacher_pk')
        return get_object_or_404(Teachers,id=pk_)

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs) 
        return context   

class TeacherUpdate(UpdateView):
    model = Teachers
    form_class = TeachersForm
    success_url = reverse_lazy('teachers_list')
    template_name = 'courses/course_form.html' 

    def get_object(self):
        pk_ = self.kwargs.get('teacher_pk')
        return get_object_or_404(Teachers,id=pk_)

    def form_valid(self,form):
        messages.success(self.request, f"Teacher updated successfully")
        return super().form_valid(form) 

    def get_success_url(self):
        return reverse_lazy('teacher_data',kwargs={'teacher_pk':CourseUpdate.get_object(self).id})

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)               
        context['title']       = 'Update Teacher'
        return context 

class TeacherDelete(DeleteView):
    model = UserAccount

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)  

    def get_object(self):        
        return get_object_or_404(UserAccount,id=self.kwargs.get('user_pk'))

    def get_success_url(self):        
        messages.success(self.request, f"Teacher deleted successfully")
        return reverse_lazy('teachers_list')


# Events

class EventsList(FilterView):
    model            = Events
    filterset_class  = EventsFilters
    template_name    = 'events/events_list.html' 

class EventData(DetailView):
    model         = Events
    template_name = 'events/events_object.html'
    
    def get_object(self):
        pk_ = self.kwargs.get('event_pk')
        return get_object_or_404(Events,id=pk_)

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs) 
        return context   

class EventCreate(CreateView):
    model  = Events
    form_class = EventForm    
    template_name = 'form.html'
    success_url = reverse_lazy('events_list')

    def form_valid(self,form):        
        messages.success(self.request, f"Event created successfully")
        return super().form_valid(form) 

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)               
        context['title']       = 'Create Event'
        return context  

    def get_success_url(self):
        title = self.request.POST['title']
        year  = self.request.POST['year']
        
        
        async_task('email_app.views.EventEmail',title,year)   
        return reverse_lazy('events_list')

class EventDelete(DeleteView):
    model = Events

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)  

    def get_object(self):        
        return get_object_or_404(Events,id=self.kwargs.get('event_pk'))

    def get_success_url(self):        
        messages.success(self.request, f"Event deleted successfully")
        return reverse_lazy('events_list')


# Assignment

class AssignmentData(DetailView):
    model = School_Assignment
    template_name = 'assignments/assignment_object.html'

    def get_object(self): 
        return get_object_or_404(School_Assignment,id=self.kwargs.get('assignment_pk')) 

        

    def get_context_data(self, **kwargs):   
        
        context = super().get_context_data(**kwargs) 

               
        try:
            id_ = AssignmentData.get_object(self) 
            s_  = Students.objects.get(user=self.request.user).id             
            if Students_Assignment.objects.filter(student=s_,assignment=id_):
                
                context['File_was_already_sent']  = True            
        except:
            context['File_was_already_sent']  = False 

        
        
        return context    

class AssignmentCreate(CreateView):
    model         = School_Assignment
    form_class    = AssignmentForm    
    template_name = 'form.html'    

    def get_object(self):              
        return  get_object_or_404(Topic,id=self.kwargs.get('topic_pk'))

    def form_valid(self,form):
        form.instance.topic = AssignmentCreate.get_object(self)        
        return super().form_valid(form) 


    def get_success_url(self):
        pk_ = AssignmentCreate.get_object(self)
        messages.success(self.request, f"assignment created successfully")         
        return reverse_lazy('topic', kwargs={'course_pk':pk_.course.id ,'topic_pk': pk_.id }) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                 
        context['title']   = 'Add Assignment'
        return context 

class Students_Assignment_list(ListView):
    model = Students_Assignment
    template_name = 'assignments/s_assignment_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        assignment  = get_object_or_404(School_Assignment,id=self.kwargs.get('assignment_pk'))
        works       = Students_Assignment.objects.filter(assignment = assignment).all()
        students    = Students.objects.filter(year = assignment.topic.course.year).all()

        total_works = 0
        for w in works:  total_works += 1

        total_students = 0 
        for s in students:  total_students += 1 

        context['works']          = works
        context['assignment']     = assignment
        context['total_works']    = total_works
        context['total_students'] = total_students
        return context

class Students_Assignment_Data(UpdateView):
    model = Students_Assignment
    form_class  = ReviewForm
    template_name = 'form.html'

    def get_object(self):
        pk_ = self.kwargs.get('homework_pk')
        return get_object_or_404(Students_Assignment,id=pk_)

    def form_valid(self, form):
        grade = self.request.POST['grade'] 
        if int(grade) >= 6: form.instance.status = 'Passed'
        else:  form.instance.status = 'Failed'

        async_task('email_app.views.Homeworkemail',Students_Assignment_Data.get_object(self).id) 


        
        return super().form_valid(form)  



    def get_success_url(self):
        pk_ =  Students_Assignment_Data.get_object(self)
        return reverse_lazy('students_assignment',kwargs={'assignment_pk':pk_.assignment.id,'course_pk':pk_.assignment.topic.course.id,'topic_pk':pk_.assignment.topic.id})   

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)               
        context['title']       = 'Review Homework'
        return context       

def Students_Assignment_Create(request,assignment_pk):    
    student = Students.objects.get(user=request.user)
    assignment = School_Assignment.objects.get(id=assignment_pk)
    Students_Assignment.objects.create(student=student,assignment=assignment,file=request.FILES['file'])
    messages.success(request,'Your homework was sent successfully.')
    return redirect('topic',course_pk=assignment.topic.course.id,topic_pk=assignment.topic.id)

# Grades

class GradesList(ListView):
    model = Students_Assignment    
    template_name = 'grades/grades_list.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        student = Students.objects.get(user=self.request.user)
        works   = Students_Assignment.objects.filter(student=student).all()  
        
        passeds = []
        faileds = []
        for w in works:
            if   w.status == 'Passed' : passeds.append(w) 
            elif w.status == 'Failed' : faileds.append(w)
     
        grades = 0
        for g in works:
            try:
                grades += g.grade 
            except:
                grades += 0    
             

        try:
            average = (int(grades)/len(works)) 
            average = round(average, 1)
        except:
            average = 0    

        context['works']   =  works
        context['passeds'] =  len(passeds)
        context['faileds'] =  len(faileds)
        context['grades']  =  grades
        context['average'] =  average
        
        return context








     


