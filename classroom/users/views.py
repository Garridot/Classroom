from django.shortcuts import render,redirect
from django.contrib.auth.forms import  PasswordChangeForm
from classroom.settings  import  EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout , authenticate
from django.contrib import messages
from django.views.generic import *
from .models import *
from .utils import RegisterForm,GetAccount
from .forms import *
import os
from email_app.views import *
# Create your views here.

# django_q




def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func


@unauthenticated_user
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


# PasswordReset

def PasswordReset(request):
    if request.method == 'POST':
        email = request.POST['email']        
        user = UserAccount.objects.filter(email=email)        
        if user:
            user = UserAccount.objects.get(email=email)             
            
            return redirect('password_reset_email_sent')
                       
        else:            
           messages.info(request,'Email not found.') 
    return render(request,'password_reset/password_reset.html')



def PasswordResetEmailSent(request):
    return render(request,'password_reset/password_reset_email_sent.html')             

def PasswordResetForm(request,email,token):
    user = UserAccount.objects.get(email= email)
    form = CreateUserForm(instance=user)
    if request.method == 'POST':
        form = CreateUserForm(request.POST,instance=user)
        if form.is_valid():                     
            form.save()    
            messages.success(request,'Password successfully restored')              
            return redirect('login')
        else:
            for msg in form.errors:
                messages.info(request,f"{msg}:{form.errors}")
    return render(request,'password_reset/password_reset_form.html',{'form':form})                



# Register

def RegisterFormView(request):
    user_form = CreateUserForm()
    form = StudentsForm()
    title = 'Apply Form'
    if request.method == 'POST':
        
        form = StudentsForm(request.POST,request.FILES)
        user_form = CreateUserForm(request.POST)
        if form.is_valid() and user_form.is_valid():   
            RegisterForm.is_valid(user_form,form)               
            return redirect('login')
        else:
            for msg in form.errors:
                return messages.error(request,f"{msg}:{form.errors}")      
        
    context={'form':form,'title':title,'user_form':user_form}    
    return render(request,'form.html',context)  




# UserProfile



class UserProfileView(DetailView):
    model         = UserAccount
    template_name = 'profile.html' 

    def get_object(self):       
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = GetAccount.get(self.request.user)
        return context


class UserProfileUpdate(UpdateView):
    success_url   = reverse_lazy('user_profile')
    model         = UserAccount
    form_class    = UserAccountForm
    template_name = 'user_update_form.html'

    def get_object(self):
        user = self.request.user
        return UserAccount.objects.get(email=user)

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs) 
        context['user'] = GetAccount.get(self.request.user)  
        return context 

    def form_valid(self, form):         
        return super().form_valid(form)    
    
        
 
@login_required(login_url='login')
def UserProfileDelete(request,email):
    user = UserAccount.objects.get(email=email)
    user.delete() 
    return redirect('login')   


# PasswordsChange
@login_required(login_url='login')
def PasswordsChange(request,email): 
    title = 'Password Change'

    form  = PasswordChangeForm(user=UserAccount.objects.get(email=email))     
    if request.method == 'POST':
        form  = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():       
            form.save()
            messages.success(request,'Password successfully updated')            
            return redirect('login')
        else: 
            for msg in form.errors:
                messages.error(request,f"{msg}:{form.errors}") 
    context = {'form':form,'title':title}
    return render(request,'form.html',context)        


