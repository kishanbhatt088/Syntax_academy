# qna/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Question, Reply

class ReplyInline(admin.TabularInline):
    """Inline admin for replies"""
    model = Reply
    extra = 0
    fields = ['user', 'content', 'is_solution', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Question Admin"""
    
    list_display = ['title_short', 'user', 'course', 'status_badge', 
                    'total_replies', 'has_admin_reply_badge', 'is_public', 'created_at']
    list_filter = ['status', 'is_public', 'course__category', 'course', 'created_at']
    search_fields = ['title', 'content', 'user__username', 'course__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    inlines = [ReplyInline]
    
    fieldsets = (
        ('Question Information', {
            'fields': ('user', 'course', 'title', 'content')
        }),
        ('Status', {
            'fields': ('status', 'is_public')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def title_short(self, obj):
        """Display shortened title"""
        return obj.title[:80] + '...' if len(obj.title) > 80 else obj.title
    title_short.short_description = 'Title'
    
    def status_badge(self, obj):
        """Display colored status badge"""
        colors = {
            'PENDING': '#ffc107',
            'ANSWERED': '#28a745',
            'CLOSED': '#6c757d'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#007bff'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def has_admin_reply_badge(self, obj):
        """Display if admin has replied"""
        if obj.has_admin_reply:
            return format_html(
                '<span style="color: #28a745;">✓ Yes</span>'
            )
        return format_html(
            '<span style="color: #dc3545;">✗ No</span>'
        )
    has_admin_reply_badge.short_description = 'Admin Replied'


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    """Reply Admin"""
    
    list_display = ['question_short', 'user', 'user_role', 'is_solution_badge', 'created_at']
    list_filter = ['user__role', 'is_solution', 'created_at']
    search_fields = ['question__title', 'content', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Reply Information', {
            'fields': ('question', 'user', 'content', 'is_solution')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_short(self, obj):
        """Display shortened question title"""
        return obj.question.title[:60] + '...' if len(obj.question.title) > 60 else obj.question.title
    question_short.short_description = 'Question'
    
    def user_role(self, obj):
        """Display user role"""
        if obj.user.is_admin:
            return format_html(
                '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px;">ADMIN</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px;">USER</span>'
        )
    user_role.short_description = 'Role'
    
    def is_solution_badge(self, obj):
        """Display solution badge"""
        if obj.is_solution:
            return format_html(
                '<span style="color: #28a745;">✓ Solution</span>'
            )
        return format_html(
            '<span style="color: #6c757d;">-</span>'
        )
    is_solution_badge.short_description = 'Solution'