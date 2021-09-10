from django.shortcuts import render
from .models import * 
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth import login, logout , authenticate

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
            [settings.EMAIL_HOST_USER],
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
