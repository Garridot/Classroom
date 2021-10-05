from django.shortcuts import HttpResponse

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*arg,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*arg,**kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator                    