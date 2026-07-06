# quiz/forms.py

from django import forms
from .models import Quiz, Question, Choice

class QuizForm(forms.ModelForm):
    """Form for creating/editing quizzes"""
    
    class Meta:
        model = Quiz
        fields = [
            'course', 'title', 'slug', 'description', 'time_limit',
            'passing_score', 'max_attempts', 'show_correct_answers',
            'randomize_questions', 'is_active', 'order'
        ]
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'passing_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_attempts': forms.NumberInput(attrs={'class': 'form-control'}),
            'show_correct_answers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'randomize_questions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_passing_score(self):
        score = self.cleaned_data.get('passing_score')
        if score is not None and (score < 0 or score > 100):
            raise forms.ValidationError('Passing score must be between 0 and 100.')
        return score

    def clean_time_limit(self):
        limit = self.cleaned_data.get('time_limit')
        if limit is not None and limit <= 0:
            raise forms.ValidationError('Time limit must be a positive number.')
        return limit

    def clean_max_attempts(self):
        attempts = self.cleaned_data.get('max_attempts')
        if attempts is not None and attempts <= 0:
            raise forms.ValidationError('Maximum attempts must be at least 1.')
        return attempts



class QuestionForm(forms.ModelForm):
    """Form for creating/editing questions"""
    
    class Meta:
        model = Question
        fields = ['quiz', 'question_text', 'explanation', 'points', 'order']
        widgets = {
            'quiz': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'points': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ChoiceForm(forms.ModelForm):
    """Form for creating/editing choices"""
    
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct', 'order']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# FormSet for handling multiple choices
from django.forms import inlineformset_factory

ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    form=ChoiceForm,
    extra=4,
    can_delete=True,
    min_num=2,
    validate_min=True,
)


class QuizAnswerForm(forms.Form):
    """Dynamic form for quiz answers"""
    
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        
        for question in questions:
            choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
            
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.question_text,
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                required=True
            )