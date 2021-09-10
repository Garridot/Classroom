from django.urls import path
from . import views

urlpatterns = [
    # path('',views.,name=''),
    path('',views.MainPage,name='main_page'),
    path('information/',views.Information,name='information'),
    path('contact/',views.Contact,name='contact'),

    path('login/',views.LoginView,name='login'),
    path('logout/',views.LogoutView,name='logout'),
]