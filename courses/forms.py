# courses/forms.py

from django import forms
from django.core.validators import FileExtensionValidator, URLValidator, MinValueValidator
from .models import Category, Course, Video, Note, Task, UserTaskProgress
import re

class CategoryForm(forms.ModelForm):
    """Form for creating/editing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'icon', 'color', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fa-python'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CourseForm(forms.ModelForm):
    """Form for creating/editing courses"""
    
    class Meta:
        model = Course
        fields = [
            'category', 'title', 'slug', 'description', 'difficulty_level',
            'thumbnail', 'estimated_duration', 'prerequisites', 
            'learning_outcomes', 'is_published', 'order'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'estimated_duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'prerequisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'learning_outcomes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class VideoForm(forms.ModelForm):
    """Form for creating/editing videos"""
    
    class Meta:
        model = Video
        fields = [
            'course', 'title', 'slug', 'description', 'video_file',
            'video_url', 'duration', 'thumbnail', 'order', 'is_preview'
        ]
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'video_file': forms.FileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/...'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_preview': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_video_url(self):
        url = self.cleaned_data.get('video_url')
        if url:
            youtube_regex = (
                r'(https?://)?(www\.)?'
                '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
            )
            vimeo_regex = r'(https?://)?(www\.)?(vimeo\.com/)\d+'
            
            if not (re.match(youtube_regex, url) or re.match(vimeo_regex, url)):
                raise forms.ValidationError('Please enter a valid YouTube or Vimeo URL.')
        return url

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if duration and duration <= 0:
            raise forms.ValidationError('Duration must be a positive number.')
        return duration
    
    def clean(self):
        cleaned_data = super().clean()
        video_file = cleaned_data.get('video_file')
        video_url = cleaned_data.get('video_url')
        
        if not video_file and not video_url:
            raise forms.ValidationError('Please provide either a video file or a video URL.')
        
        return cleaned_data


class NoteForm(forms.ModelForm):
    """Form for creating/editing notes"""
    
    class Meta:
        model = Note
        fields = ['course', 'title', 'slug', 'content', 'order']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TaskForm(forms.ModelForm):
    """Form for creating/editing tasks"""
    
    class Meta:
        model = Task
        fields = [
            'course', 'title', 'slug', 'description', 'task_file',
            'difficulty', 'estimated_time', 'order'
        ]
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'task_file': forms.FileInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'estimated_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TaskSubmissionForm(forms.ModelForm):
    """Form for students to submit their tasks"""
    
    class Meta:
        model = UserTaskProgress
        fields = ['submission_file']
        widgets = {
            'submission_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.docx,.txt,.jpg,.jpeg,.png,.zip'
            }),
        }
    
    def clean_submission_file(self):
        file = self.cleaned_data.get('submission_file')
        if not file:
            raise forms.ValidationError('Please select a file to upload.')
        
        # Limit file size (e.g., 5MB)
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File size must be under 5MB.')
            
        return file