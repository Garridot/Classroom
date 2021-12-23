from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.LoginView,name='login'),
    path('logout/',views.LogoutView,name='logout'),
    path('register/',views.RegisterFormView,name='register'),

    path('password_reset/',views.PasswordReset,name='password_reset'),
    path('password_reset_email_sent/',views.PasswordResetEmailSent,name='password_reset_email_sent'),
    path('password_reset_form/<str:email>/<token>',views.PasswordResetForm,name='password_reset_form'),


    path('user_profile',views.UserProfileView.as_view(),name='user_profile'),
    path('user_profile/update/',views.UserProfileUpdate.as_view(),name='user_update'),
    path('user_profile/delete/<str:email>',views.UserProfileDelete,name='user_profile_delete'),

    path('password_change/<str:email>',views.PasswordsChange,name='password_change'),

]