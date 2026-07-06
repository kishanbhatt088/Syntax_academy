# qna/forms.py

from django import forms
from .models import Question, Reply

class QuestionForm(forms.ModelForm):
    """Form for creating/editing questions"""
    
    class Meta:
        model = Question
        fields = ['course', 'title', 'content', 'is_public']
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your question title',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe your question in detail...',
                'required': True
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'is_public': 'Make this question visible to other students',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 10:
            raise forms.ValidationError('Title must be at least 10 characters long.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 20:
            raise forms.ValidationError('Content must be at least 20 characters long.')
        return content
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter courses to show only enrolled courses for the user
        if user and not user.is_admin:
            from courses.models import Enrollment
            enrolled_course_ids = Enrollment.objects.filter(
                user=user
            ).values_list('course_id', flat=True)
            
            self.fields['course'].queryset = self.fields['course'].queryset.filter(
                id__in=enrolled_course_ids
            )


class ReplyForm(forms.ModelForm):
    """Form for creating/editing replies"""
    
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your reply...',
                'required': True
            }),
        }
        labels = {
            'content': 'Your Reply',
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise forms.ValidationError('Reply must be at least 5 characters long.')
        return content


class AdminReplyForm(forms.ModelForm):
    """Form for admin replies with solution option"""
    
    class Meta:
        model = Reply
        fields = ['content', 'is_solution']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your reply...',
                'required': True
            }),
            'is_solution': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'content': 'Your Reply',
            'is_solution': 'Mark this as the solution',
        }


class QuestionStatusForm(forms.ModelForm):
    """Form for updating question status (admin only)"""
    
    class Meta:
        model = Question
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }