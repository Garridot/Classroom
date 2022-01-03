from .models import *
from .forms import *  
from .forms import *
from .views import *



class RegisterForm():
    def is_valid(user_form,form):  
            
            user_form.save()
            form.instance.user = UserAccount.objects.get(email=user_form.instance.email)
            form.save()  
            
class GetAccount():
    def get(user):
        if Students.objects.filter(user=user).exists(): return Students.objects.get(user=user)
        elif Teachers.objects.filter(user=user).exists(): return Teachers.objects.get(user=user)
        else: return None
        
   
    

# class Updatepicture():
#     def update(profile_picture,account):
#         if len(profile_picture)!= 0:            
#             if len(profile_picture)> 0:
#                 os.remove(account.profile_picture.path)
#             account.profile_picture = request.FILES['profile_picture']  
                            
            