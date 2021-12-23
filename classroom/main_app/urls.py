from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.MainPage,name='main_page'),
    path('information/',views.Information,name='information'),
    path('contact/',views.Contact,name='contact'),

    path('home/',views.HomeView,name='home'),

    path('courses/',views.CoursesList.as_view(),name='courses'),
    path('courses/create',views.CourseCreate.as_view(),name='course_create'),    
    path('courses/<str:course_pk>/',views.CourseData.as_view(),name='course_data'),    
    path('courses/<str:course_pk>/update',views.CourseUpdate.as_view(),name='course_update'),
    path('courses/<str:course_pk>/delete',views.CourseDelete.as_view(),name='course_delete'),


    path('courses/<str:course_pk>/topics/<str:topic_pk>/',views.TopicDetail.as_view(),name='topic'),
    path('courses/<str:course_pk>/topic/create/',views.TopicCreate.as_view(),name='topic_create'),
    path('courses/<str:course_pk>/topics/<str:topic_pk>/update',views.TopicUpdate.as_view(),name='topic_update'),
    path('courses/<str:course_pk>/topics/<str:topic_pk>/delete',views.TopicDelete.as_view(),name='topic_delete'),


    path('courses/<str:course_pk>/topic/<str:topic_pk>/content/create/',views.ContentCreate.as_view(),name='content_create'),
    path('courses/<str:course_pk>/topic/<str:topic_pk>/content/<str:content_pk>/delete/',views.ContentDelete.as_view(),name='content_delete'),


    path('courses/<str:course_pk>/topic/<str:topic_pk>/assignment/create',views.AssignmentCreate.as_view(),name='assignment_create'),
    path('courses/<str:course_pk>/topic/<str:topic_pk>/assignment/<str:assignment_pk>',views.AssignmentData.as_view(),name='assignment_data'),
    

    path('students',views.StudentsList.as_view(),name='students_list'),
    path('student_create',views.StudentCreate,name='student_create'),
    path('students/<str:student_pk>',views.StudentData.as_view(),name='student_data'),
    path('students/<str:student_pk>/update',views.StudentUpdate.as_view(),name='student_update'),
    path('students/<str:student_pk>/delete',views.StudentDelete.as_view(),name='student_delete'),


    path('teachers',views.TeachersList.as_view(),name='teachers_list'),
    path('teachers/create',views.TeacherCreate,name='teachers_create'),
    path('teachers/<str:teacher_pk>',views.TeacherData.as_view(),name='teacher_data'),
    path('teachers/<str:teacher_pk>/update',views.TeacherUpdate.as_view(),name='teacher_update'),
    path('teachers/<str:teacher_pk>/delete',views.TeacherDelete.as_view(),name='teacher_delete'),


    path('events',views.EventsList.as_view(),name='events_list'),
    path('events/create',views.EventCreate.as_view(),name='event_create'),
    path('events/<str:event_pk>',views.EventData.as_view(),name='event_data'),
    path('events/<str:event_pk>/delete',views.EventDelete.as_view(),name='event_delete'),


    path('courses/<str:course_pk>/topic/<str:topic_pk>/assignments/create',views.AssignmentCreate.as_view(),name='assignment_create'),
    path('courses/<str:course_pk>/topic/<str:topic_pk>/assignments/<str:assignment_pk>',views.AssignmentData.as_view(),name='assignments_list'),
    path('courses/<str:course_pk>/topic/<str:topic_pk>/assignments/<str:assignment_pk>/students_assignment',views.Students_Assignment_list.as_view(),name='students_assignment'),
    path('courses/<str:course_pk>/topic/<str:topic_pk>/assignments/<str:assignment_pk>/students_assignment/<str:homework_pk>',views.Students_Assignment_Data.as_view(),name='student_homework'),
    path('assignment/<str:assignment_pk>/send',views.Students_Assignment_Create,name='send_homework'),
    
    
    path('grades',views.GradesList.as_view(),name='grades_list'),
    
    path('recent_content/',views.HistoryView,name=''),

]