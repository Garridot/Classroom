from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserForm(UserCreationForm):    
    class Meta:               
        model  = UserAccount
        exclude = ('password','user_permissions','groups','is_active','is_staff','is_superuser','is_teacher','is_student','is_admin')
