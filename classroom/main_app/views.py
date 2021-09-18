from django.http import request
from classroom.settings  import  EMAIL_HOST_USER

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import send_mail

from django.contrib.auth import login, logout , authenticate
from django.shortcuts import render,redirect
from django.contrib import messages
from calendar import HTMLCalendar


from .models import * 
from .forms import *
from .utils import *
from .filters import*

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


def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')        
        user = authenticate(request , email = email, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')            
        else:           
            messages.info(request,'Email or password is incorrect.') 
    return render(request,'login.html')
def LogoutView(request):     
    logout(request)
    return redirect('login') 


def PasswordReset(request):
    if request.method == 'POST':
        email = request.POST['email']        
        user = UserAccount.objects.filter(email=email)        
        if user:
            user = UserAccount.objects.get(email=email)  
            PasswordResetEmail(user)
            return redirect('password_reset_email_sent')
                       
        else:            
           messages.info(request,'Email not found.') 
    return render(request,'password_reset/password_reset.html')
def PasswordResetEmail(user): 
    from django.contrib.auth.tokens import PasswordResetTokenGenerator
    password_reset_token = PasswordResetTokenGenerator().make_token(user)   
    context = {'user':user,'token':password_reset_token}
    template  = get_template('password_reset/password_reset_email.html')
    content   = template.render(context)
    email     = EmailMultiAlternatives(
        'AcademiaWeb',
        'Password Reset',
        EMAIL_HOST_USER,
        [user.email]
    )
    email.attach_alternative(content,'text/html')
    email.send()
def PasswordResetEmailSent(request):
     return render(request,'password_reset/password_reset_email_sent.html')             
def PasswordResetForm(request,email,token):
    user = UserAccount.objects.get(email= email)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():                     
            form.save()            
            return redirect('password_reset_done',email=email)
        else:
            for msg in form.errors:
                messages.info(request,f"{msg}:{form.errors}")
    return render(request,'password_reset/password_reset_form.html',{'form':form})                
def PasswordResetDone(request,email):
    return render(request,'password_reset/password_reset_done.html',{'email':email})

def ApplicationsFormView(request):
    form = ApplicationsForm()
    if request.method == 'POST':
        form = ApplicationsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            ApplicationSendEmail(email=form.instance.email)            
            return redirect('application_send',pk=form.instance.email)
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}")   
    context={'form':form}
    return render(request,'form.html',context)  
def ApplicationSend(request,pk):
    admission = Applications.objects.get(email=pk)
    context={'admission':admission}
    return render(request,'application_send.html',context) 
def ApplicationSendEmail(email):
    admission = Applications.objects.get(email=email)  
    context   = {'email':email,'admission':admission}     
    template  = get_template('emails/application_send_email.html')
    content   = template.render(context)

    email     = EmailMultiAlternatives(
        'Request received!',
        'Your application has been successfully submitted.',
        EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(content,'text/html')
    email.send()

def HomeView(request):
    data = user_profile(request)
    user = data['user']
    notifications = Notifications.objects.all()

    year     = timezone.now().year
    month    = timezone.now().month
    calendar = HTMLCalendar().formatmonth(theyear=year,themonth=month) 
    events   = Events.objects.filter(event_date__month=month).all()  

    if request.user.is_admin:
        info = Applications.objects.order_by('-sent_date').all()
    

    context = {'notifications':notifications,
        'user':user,'calendar':calendar,'info':info,
        'events':events,        
    }

    return render(request,'home.html',context) 

def UserProfileView(request,full_name):
    data = user_profile(request)
    user = data['user']
    context = {'user':user}
    return render(request,'profile.html',context)

def AdmissionsView(request):
    data = user_profile(request)
    user = data['user']

    requests = Applications.objects.all()
    filters  = ApplyFilters(request.GET,queryset=requests)
    requests = filters.qs     
    title    = 'Admissions'
    request_data = 'admission_data'      
    context  = {'requests':requests,'filters':filters,'title':title,'request_data':request_data,'user':user}
    return render(request,'request_list.html',context)
def AdmissionData(request,email):
    admission = Applications.objects.get(email=email)   
    context = {'admission':admission}
    return render(request,'admission_profile.html',context)
def AdmissionAccept(request,email):
    admission = Applications.objects.get(email=email)     
    info = f'The student needs a password.\nTips:\nemail: {admission.email}\npassword: {admission.first_name}{admission.last_name}{admission.document}'
    user_form = UserForm()
    form = StudentsForm(instance=admission)
    if request.method=='POST':
        user_form = UserForm(request.POST)
        form      = StudentsForm(request.POST,request.FILES)
        if user_form.is_valid():
            user_form.save()
            user = UserAccount.objects.get(email=user_form['email'].value()) 
            form.instance.user = user 
            form.save()
            AdmissionEMAIL(email)            
            return redirect('home')
        

    context = {'info':info,'form':form,'user_form':user_form}
    return render(request,'form.html',context)

def AdmissionEMAIL(email):
    admission = Applications.objects.get(email=email)  
    context   = {'email':email,'admission':admission}     
    template  = get_template('emails/application_accepted.html')
    content   = template.render(context)

    email     = EmailMultiAlternatives(
        f'Congratulations {admission.full_name}!',
        'Your application has been successfully accepted.',
        EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(content,'text/html')
    email.send()
def AdmissionDenied(email): 
    admission = Applications.objects.get(email=email)  
    context   = {'email':email,'admission':admission}     
    template  = get_template('emails/application_denied.html')
    content   = template.render(context)

    email     = EmailMultiAlternatives(
        'Student not chosen',
        'Your application has been successfully denied.',
        EMAIL_HOST_USER,
        [email]
    )
    email.attach_alternative(content,'text/html')
    email.send()       

def StudentsView(request):
    data = user_profile(request)
    user = data['user']
    students = Students.objects.all()
    filters  = StudentsFilters(request.GET,queryset=students)
    students = filters.qs     
    title    = 'Students'         
    context  = {'students':students,'filters':filters,'title':title,'user':user}
    return render(request,'request_list.html',context)
def StudentData(request,email):
    user = UserAccount.objects.get(email=email)
    user = Students.objects.get(user = user)
    context = {'user':user}
    return render(request,'profile.html',context)

def AdminsView(request):
    data = user_profile(request)
    user = data['user']
    requests = Admins.objects.all()
    filters  = ApplyFilters(request.GET,queryset=requests)
    requests = filters.qs     
    title    = 'Admins'
    request_data = 'admin_data'      
    context  = {'requests':requests,'filters':filters,'title':title,'request_data':request_data,'user':user}
    return render(request,'request_list.html',context)    

def TeachersView(request):  
    data = user_profile(request)
    user = data['user']
    teachers = Teachers.objects.all()
    filters  = TeachersFilters(request.GET,queryset=teachers) 
    teachers = filters.qs     
    title    = 'Teachers'     
    create_url   =  'teacher_create'     
    context  = {'teachers':teachers,'filters':filters,'title':title,'user':user,'create_url':create_url}
    return render(request,'request_list.html',context)    
def TeacherCreate(request):
    user_form = UserForm()
    title     = 'Add Teacher Account'
    form     = TeachersForm()
    if request.method == 'POST':
        form = TeachersForm(request.POST,request.FILES)
        user_form = UserForm(request.POST)
        if form.is_valid() and user_form.is_valid(): 
            user_form.instance.is_teacher = True    
            user_form.save()
            email = user_form['email'].value()            
            user   = UserAccount.objects.get(email=email)             
            form.instance.user = user
            form.save()  
            # create_teacher(user_form,form)
            messages.success(request,'Teacher created successfully.')
            return redirect('teachers')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 

    context = {'form':form,'user_form':user_form,'title':title}
    return render (request,'form.html',context) 
def TeacherData(request,email):
    user_teacher  = UserAccount.objects.get(email=email)
    teacher_account = Teachers.objects.get(user=user_teacher)
    context = {'user':teacher_account}
    return render(request,'profile.html',context)
def TeacherDelete(request,email):
    user  = UserAccount.objects.get(email=email)
    user.delete()
    messages.success(request,'Teacher deleted successfully.')
    return redirect('teachers')  

def AdminsView(request):
    data = user_profile(request)
    user = data['user']
    admins  = Admins.objects.all()
    filters = AdminsFilters(request.GET,queryset=admins) 
    admins  = filters.qs
    title   = 'Admins'
    create_url = 'admin_create'
    context  = {'admins':admins,'filters':filters,'title':title,'user':user,'create_url':create_url}
    return render(request,'request_list.html',context)    
def AdminsData(request,email):
    user_teacher  = UserAccount.objects.get(email=email)
    admin_account = Admins.objects.get(user=user_teacher)
    context = {'user':admin_account}
    return render(request,'profile.html',context)
def AdminCreate(request):
    user_form = UserForm()
    title     = 'Add Teacher Account'
    form      =  AdminsForm()
    if request.method == 'POST':
        form = AdminsForm(request.POST,request.FILES)
        user_form = UserForm(request.POST)
        if form.is_valid() and user_form.is_valid(): 
            user_form.instance.is_admin = True    
            user_form.save()
            email = user_form['email'].value()            
            user   = UserAccount.objects.get(email=email)             
            form.instance.user = user
            form.save()              
            messages.success(request,'Admin successfully created.')
            return redirect('admins')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 

    context = {'form':form,'user_form':user_form,'title':title}
    return render (request,'form.html',context) 


def CoursesView(request):
    data = user_profile(request)
    user = data['user']
    courses = Courses.objects.all()
    filters  = CoursesFilters(request.GET,queryset=courses) 
    courses = filters.qs     
    title    = 'Courses'     
    create_url   =  'course_create'     
    context  = {'courses':courses,'filters':filters,'title':title,'user':user,'create_url':create_url}
    return render(request,'request_list.html',context)  
def CourseCreate(request):    
    form     = CoursesForm()
    title    = 'Create Course'
    if request.method == 'POST':
        form     = CoursesForm(request.POST,request.FILES)        
        if form.is_valid(): 
            form.save()
            messages.success(request,'Course successfully created.')
            return redirect('courses')
        else:
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 
    context = {'form':form,'title':title}        
    return render (request,'form.html',context)
def CourseData(request,name,year):
    course = Courses.objects.get(name=name,year=year)
    teachers = Teachers.objects.filter(courses=course).all()
    categories = CourseCategory.objects.filter(course=course).all()     
    context =  {'course':course,'teachers':teachers,'categories':categories}
    return render(request,'course_data.html',context)
def CourseDelete(request,name,year):
    course = Courses.objects.get(name=name,year=year)    
    course.delete()
    messages.success(request,'Course successfully deleted.')
    return redirect('courses') 

def CategoriesView(request,course,category):
    course   = Courses.objects.get(name=course)
    category = CourseCategory.objects.get(course = course,name=category)
    contents  = Content.objects.filter(category=category).all()
    context  = {'course':course,'category':category,'contents':contents}
    return render(request,'category_data.html',context) 
def CategoryCreate(request,course):
    course = Courses.objects.get(name=course)
    form   = CategoryForm()
    title  = 'Add Category'
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.instance.course = course
            form.instance.year   = course.year
            form.save()
            Notifications.objects.create(user=request.user,message=f"{course.name} : A new category has been added!",year=course.year) 
    context= {'form':form,'title':title}
    return render(request,'form.html',context) 
def ContentAdd(request,course,category):
    category = CourseCategory.objects.get(name=category)
    course   = Courses.objects.get(name=course)
    form  = ContentForm()
    title = 'Add content'
    if request.method == 'POST':
        form = ContentForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.category = category
            form.save()
            Notifications.objects.create(user=request.user,message=f"{course.name} / {category.name} : New content has been added!",year=course.year) 
            return redirect('category',course=course.name,category=category.name)
    context= {'form':form,'title':title}
    return render(request,'form.html',context) 

def YearsViews(request):
    data = user_profile(request)
    user = data['user']
    years = SchoolYears.objects.all()    
    title    = 'SchoolYears'     
    create_url   =  'year_create'     
    context  = {'years':years,'title':title,'user':user,'create_url':create_url}
    return render(request,'request_list.html',context)  
def YearData(request,pk):
    year = SchoolYears.objects.get(id=pk)
    students  = Students.objects.filter(year = year)
    courses   = Courses.objects.filter(year = year)
    admssions = Applications.objects.filter(year=year)
    context   = {'year':year,'students':students,'courses':courses,'admssions':admssions}
    return render(request,'year_data.html',context)  

def EventsView(request):
    data = user_profile(request)
    user    = data['user']   
    events  = data['events']  
    filters = EventsFilters(request.GET,queryset=events)
    title   = 'Events'
    request_data = 'event'
    create_url = 'event_create'
    context = {'user':user,'events':events,'filters':filters,'title':title,'request_data':request_data,'create_url':create_url}
    return render(request,'request_list.html',context)
def EventData(request,title,date):
    event = Events.objects.get(title=title,event_date=date)
    comments = Comments.objects.filter(event=event)
    total_comments = 0
    for comment in comments:
        total_comments += 1
    context = {'event':event,'comments':comments,'total_comments':total_comments}
    return render(request,'event_data.html',context)
def CommentAdd(request,pk):
    event = Events.objects.get(id=pk)
    if request.method == 'POST':
        message = request.POST['message']
        Comments.objects.create(
            event        = event,
            user         = request.user,
            menssage     = message         
        )
    return redirect('event',title=event.title, date=event.event_date)
def CommentDelete(request,pk):
    comment = Comments.objects.get(id=pk)    
    comment.delete()
    event     = Events.objects.get(id=comment.event.id)
    return redirect('event',title=event.title, date=event.event_date)
def EventCreate(request):
    form = EventForm()
    title = 'Add Event'
    if request.method == 'POST':
        form = EventForm(request.POST,)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            year = SchoolYears.objects.get(id=request.POST['year'])
            Notifications.objects.create(user=request.user,message=f"New event added!",year=year) 
            messages.success(request,'Event successfully added')
            return redirect('events')
    context={'form':form,'title':title}
    return render(request,'form.html',context)


