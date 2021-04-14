from django.http import HttpResponse
from django.shortcuts import redirect


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('user-dashboard')

        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
    return wrapper_function
