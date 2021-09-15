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

    path('home/',views.HomeView,name='home'),

    path('user_profile/name=<str:full_name>/',views.UserProfileView,name='user_profile'),

    path('admissions/',views.AdmissionsView,name='admissions'),
    path('admissions/admission_data/email=<str:email>',views.AdmissionData,name='admission'),
    path('admissions/admission_accept/email=<str:email>',views.AdmissionAccept,name='admission_accept'),
    path('admissions/admission_denied/email=<str:email>',views.AdmissionDenied,name='admission_denied'),

    path('students/',views.StudentsView,name='students'),
    path('students/student/email=<str:email>',views.StudentData,name='student'),

    path('teachers/',views.TeachersView,name='teachers'),
    path('teachers/teacher_create/',views.TeacherCreate,name='teacher_create'),    
    path('teacher/<str:email>/',views.TeacherData,name='teacher'),
    path('teacher_delete/<str:email>/',views.TeacherDelete,name='delete_teacher'),

      
]