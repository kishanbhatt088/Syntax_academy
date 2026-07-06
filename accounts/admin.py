# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'bio', 'profile_picture')}),
        (_('Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User Profile Admin"""
    
    list_display = ['user', 'city', 'country', 'courses_completed', 'total_learning_hours']
    list_filter = ['country', 'city']
    search_fields = ['user__username', 'user__email', 'city', 'country']
    
    fieldsets = (
        (_('User Information'), {
            'fields': ('user',)
        }),
        (_('Location'), {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        (_('Social Links'), {
            'fields': ('github_profile', 'linkedin_profile', 'website')
        }),
        (_('Statistics'), {
            'fields': ('total_learning_hours', 'courses_completed', 'total_quiz_score')
        }),
    )
    
    readonly_fields = ['total_learning_hours', 'courses_completed', 'total_quiz_score']