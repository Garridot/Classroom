from django.urls import path
from . import views

urlpatterns = [
    # path('',views.,name=''),
    path('',views.MainPage,name='main_page'),
    path('information/',views.Information,name='information'),
    path('contact/',views.Contact,name='contact'),

    path('login/',views.LoginView,name='login'),
    path('logout/',views.LogoutView,name='logout'),

    path('password_reset/',views.PasswordReset,name='password_reset'),
    path('password_reset_email_sent/',views.PasswordResetEmailSent,name='password_reset_email_sent'),
    path('password_reset_form/<str:email>/<token>',views.PasswordResetForm,name='password_reset_form'),
    path('password_reset_done/<str:email>',views.PasswordResetDone,name='password_reset_done'),

    path('applications_form/',views.ApplicationsFormView,name='applications_form'),
    path('application_send/<str:pk>',views.ApplicationSend,name='application_send'), 

    path('home/',views.HomeView,name='home')  
]