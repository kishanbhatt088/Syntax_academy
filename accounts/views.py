# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

User = get_user_model()


def register_view(request):
    """User Registration"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard:admin')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        errors = []
        
        if not username or not email or not password1:
            errors.append('All fields are required.')
        
        if password1 != password2:
            errors.append('Passwords do not match.')
        
        if len(password1) < 6:
            errors.append('Password must be at least 6 characters.')
        
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        
        if User.objects.filter(email=email).exists():
            errors.append('Email already registered.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                is_approved=False,  # New users require approval
            )
            
            messages.success(request, f'Account created successfully! Your account is pending admin approval. You will be able to login once approved.')
            return redirect('accounts:login')
    
    return render(request, 'accounts/register.html', {'title': 'Register'})


def login_view(request):
    """
    Login View - Same page for Admin and User
    After login:
    - Admin/Staff users → Admin Dashboard
    - Regular users → User Dashboard
    """
    # If already logged in, redirect based on role
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard:admin')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        # Try to authenticate with username
        user = authenticate(request, username=username, password=password)
        
        # If failed, try with email
        if user is None:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            if not user.is_approved:
                messages.error(request, 'Your account is pending admin approval. Please wait for the administrator to activate your account.')
                return render(request, 'accounts/login.html', {'title': 'Login'})

            login(request, user)
            
            # Set session expiry
            if not remember_me:
                request.session.set_expiry(0)  # Expires on browser close
            
            messages.success(request, f'Welcome back, {user.username}!')
            
            # ===========================
            # ROLE-BASED REDIRECT
            # ===========================
            if user.is_staff or user.is_superuser:
                # Admin user → Admin Dashboard
                return redirect('dashboard:admin')
            else:
                # Regular user → User Dashboard
                next_url = request.GET.get('next', 'dashboard:home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username/email or password.')
    
    return render(request, 'accounts/login.html', {'title': 'Login'})


def logout_view(request):
    """Logout and redirect to home"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


from .forms import UserUpdateForm, UserProfileUpdateForm
from .models import UserProfile

@login_required
def profile_view(request):
    """View and edit profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {
        'title': 'My Profile',
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def change_password_view(request):
    """Change password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('accounts:profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {
        'form': form,
        'title': 'Change Password'
    })