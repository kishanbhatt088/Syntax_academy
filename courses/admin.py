# courses/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Course, Video, Note, Task, 
    UserVideoProgress, UserNoteProgress, UserTaskProgress, Enrollment
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""
    
    list_display = ['name', 'slug', 'colored_badge', 'total_courses', 'is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Display Settings', {
            'fields': ('icon', 'color', 'order', 'is_active')
        }),
    )
    
    def colored_badge(self, obj):
        """Display colored badge"""
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            obj.color,
            obj.name
        )
    colored_badge.short_description = 'Badge Preview'
    
    def total_courses(self, obj):
        """Display total courses count"""
        return obj.total_courses
    total_courses.short_description = 'Total Courses'


class VideoInline(admin.TabularInline):
    """Inline admin for videos"""
    model = Video
    extra = 0
    # REMOVE prepopulated_fields from inline - it causes the error
    fields = ['title', 'order', 'duration', 'is_preview']
    # Don't use prepopulated_fields in inline forms
    # prepopulated_fields = {'slug': ('title',)}  # ← REMOVE THIS LINE


class NoteInline(admin.TabularInline):
    """Inline admin for notes"""
    model = Note
    extra = 0
    fields = ['title', 'order']
    # prepopulated_fields = {'slug': ('title',)}  # ← REMOVE THIS LINE


class TaskInline(admin.TabularInline):
    """Inline admin for tasks"""
    model = Task
    extra = 0
    fields = ['title', 'difficulty', 'order']
    # prepopulated_fields = {'slug': ('title',)}  # ← REMOVE THIS LINE


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Course Admin"""
    
    list_display = ['title', 'category', 'difficulty_level', 'is_published', 
                    'total_videos', 'total_notes', 'total_tasks', 'created_at']
    list_filter = ['category', 'difficulty_level', 'is_published', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['category', 'order', 'title']
    
    inlines = [VideoInline, NoteInline, TaskInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'description', 'thumbnail')
        }),
        ('Course Details', {
            'fields': ('difficulty_level', 'estimated_duration', 'prerequisites', 'learning_outcomes')
        }),
        ('Settings', {
            'fields': ('is_published', 'order', 'created_by')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Auto-set created_by field"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Video Admin"""
    
    list_display = ['title', 'course', 'duration', 'is_preview', 'order', 'created_at']
    list_filter = ['course__category', 'course', 'is_preview', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    prepopulated_fields = {'slug': ('title',)}  # ← This is OK in main admin
    ordering = ['course', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'title', 'slug', 'description', 'thumbnail')
        }),
        ('Video Source', {
            'fields': ('video_file', 'video_url'),
            'description': 'Upload a video file OR provide a video URL (YouTube/Vimeo)'
        }),
        ('Settings', {
            'fields': ('duration', 'order', 'is_preview')
        }),
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Note Admin"""
    
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course__category', 'course', 'created_at']
    search_fields = ['title', 'content', 'course__title']
    prepopulated_fields = {'slug': ('title',)}  # ← This is OK in main admin
    ordering = ['course', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'title', 'slug')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Settings', {
            'fields': ('order',)
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Task Admin"""
    
    list_display = ['title', 'course', 'difficulty', 'estimated_time', 'order', 'created_at']
    list_filter = ['course__category', 'course', 'difficulty', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    prepopulated_fields = {'slug': ('title',)}  # ← This is OK in main admin
    ordering = ['course', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'title', 'slug', 'description')
        }),
        ('Task Details', {
            'fields': ('task_file', 'difficulty', 'estimated_time')
        }),
        ('Settings', {
            'fields': ('order',)
        }),
    )


@admin.register(UserVideoProgress)
class UserVideoProgressAdmin(admin.ModelAdmin):
    """User Video Progress Admin"""
    
    list_display = ['user', 'video', 'is_completed', 'watch_time_display', 'completed_at']
    list_filter = ['is_completed', 'video__course', 'created_at']
    search_fields = ['user__username', 'video__title']
    readonly_fields = ['watch_time', 'last_position', 'created_at', 'updated_at']
    
    def watch_time_display(self, obj):
        """Display watch time in minutes"""
        minutes = obj.watch_time // 60
        seconds = obj.watch_time % 60
        return f"{minutes}m {seconds}s"
    watch_time_display.short_description = 'Watch Time'


@admin.register(UserNoteProgress)
class UserNoteProgressAdmin(admin.ModelAdmin):
    """User Note Progress Admin"""
    
    list_display = ['user', 'note', 'is_read', 'read_at']
    list_filter = ['is_read', 'note__course', 'read_at']
    search_fields = ['user__username', 'note__title']
    readonly_fields = ['read_at']


@admin.register(UserTaskProgress)
class UserTaskProgressAdmin(admin.ModelAdmin):
    """User Task Progress Admin"""
    
    list_display = ['user', 'task', 'is_completed', 'has_submission', 'completed_at']
    list_filter = ['is_completed', 'task__course', 'completed_at']
    search_fields = ['user__username', 'task__title']
    readonly_fields = ['completed_at', 'submission_file_link']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'task', 'is_completed')
        }),
        ('Submission Details', {
            'fields': ('submission_file', 'submission_file_link', 'completed_at')
        }),
    )

    def has_submission(self, obj):
        return bool(obj.submission_file)
    has_submission.boolean = True
    has_submission.short_description = 'Submitted'

    def submission_file_link(self, obj):
        if obj.submission_file:
            return format_html('<a href="{}" target="_blank">View Submission</a>', obj.submission_file.url)
        return "No submission"
    submission_file_link.short_description = 'Submission Link'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Enrollment Admin"""
    
    list_display = ['user', 'course', 'progress_percentage', 'is_completed', 'enrolled_at']
    list_filter = ['is_completed', 'course__category', 'enrolled_at']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['enrolled_at', 'progress_percentage']
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly"""
        if obj:  # Editing existing object
            return self.readonly_fields + ['user', 'course']
        return self.readonly_fields