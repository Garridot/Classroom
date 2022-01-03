from django.shortcuts import render,redirect
from django.contrib.auth.forms import  PasswordChangeForm
from classroom.settings  import  EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout , authenticate
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import *
from .models import *
from .utils import RegisterForm,GetAccount
from .forms import *
import os

from email_app.views import *
# Create your views here.


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
            PasswordResetEmail(user)
            return redirect('password_reset_email_sent')
                       
        else:            
           messages.info(request,'Email not found.') 
    return render(request,'password_reset/password_reset.html')



def PasswordResetEmailSent(request):
    return render(request,'password_reset/password_reset_email_sent.html')             

def PasswordResetForm(request,email,token):
    user = UserAccount.objects.get(email= email)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
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
    user_form = UserForm()
    form = StudentsForm()
    title = 'Apply Form'
    if request.method == 'POST':
        
        form = StudentsForm(request.POST,request.FILES)
        user_form = UserForm(request.POST)

        if form.is_valid() and user_form.is_valid():   
            RegisterForm.is_valid(user_form,form)            
            RegisterEMAIL(email=user_form.instance.email)            
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

# class UserProfileUpdate(View):        
#     success_url   = reverse_lazy('user_profile')     

#     def get(self,request):
#         context = {}        
#         context['form'] = GetAccount.get_instance(self.request.user)
#         return render(request,'user_update_form.html',context)

#     def post(self,form):
#         return UserProfileUpdate.form_valid(form)

#     def form_valid(self, form):
#         # profile_picture = self.request.FILES['profile_picture']
#         # print(form)
#         # if len(profile_picture)!= 0:            
#         #     if len(profile_picture)> 0:
#         #         os.remove(form.profile_picture.path)
#         #     form.profile_picture = request.FILES['profile_picture']    
#         return reverse_lazy('user_profile') 



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
    
        
    

# @login_required(login_url='login')
# def UserProfileUpdate(request,email):
    
#     user = UserAccount.objects.get(email=email)        
#     form = UpdateUserForm(instance=user)

#     if request.method == 'POST':
#         form  = UpdateUserForm(request.POST,instance=user)
#         profile_picture = request.FILES['profile_picture']
#         if form.is_valid():       
#             form.save()  
#             Updatepicture.update(profile_picture,account)          
#             account.save()
#             messages.success(request,'Account successfully update!')
#             return redirect('home')
#     context = {'user':user,'account':account,'form':form}
#     return render (request,'user_update_form.html',context)

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


