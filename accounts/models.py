# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User Model extending Django's AbstractUser
    """
    
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        USER = 'USER', _('User')
    
    # Add related_name to fix the clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set',  # ← Changed from 'user_set'
        related_query_name='custom_user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set',  # ← Changed from 'user_set'
        related_query_name='custom_user',
    )
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name=_('User Role')
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name=_('Email Address')
    )
    
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('Phone Number')
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name=_('Profile Picture')
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_('Biography')
    )
    
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Date of Birth')
    )
    
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name=_('Email Verified')
    )
    
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_('Is Approved')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        """Check if user is admin"""
        return self.role == self.Role.ADMIN
    
    @property
    def is_regular_user(self):
        """Check if user is regular user"""
        return self.role == self.Role.USER
    
    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.username


class UserProfile(models.Model):
    """
    Extended profile information for users
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )
    
    address = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_('Address')
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('City')
    )
    
    state = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('State')
    )
    
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Country')
    )
    
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Postal Code')
    )
    
    github_profile = models.URLField(
        blank=True,
        verbose_name=_('GitHub Profile')
    )
    
    linkedin_profile = models.URLField(
        blank=True,
        verbose_name=_('LinkedIn Profile')
    )
    
    website = models.URLField(
        blank=True,
        verbose_name=_('Website')
    )
    
    total_learning_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Total Learning Hours')
    )
    
    courses_completed = models.IntegerField(
        default=0,
        verbose_name=_('Courses Completed')
    )
    
    total_quiz_score = models.IntegerField(
        default=0,
        verbose_name=_('Total Quiz Score')
    )
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"Profile of {self.user.username}"