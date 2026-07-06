# accounts/decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """
    Decorator to check if user is admin
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this page.')
            return redirect('accounts:login')
        
        # Check if user is staff/superuser (works without custom User model)
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard:home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def user_required(view_func):
    """
    Decorator to check if user is regular user (not admin)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this page.')
            return redirect('accounts:login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def anonymous_required(view_func):
    """
    Decorator to check if user is NOT logged in
    Redirects to dashboard if already logged in
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('dashboard:admin')
            else:
                return redirect('dashboard:home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
