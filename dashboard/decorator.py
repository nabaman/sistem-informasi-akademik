from django.shortcuts import redirect

def unauthenticated_user(view_function):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        else:
            return view_function(request,*args,**kwargs)

    return wrapper_function
