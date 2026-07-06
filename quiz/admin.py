# quiz/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Quiz, Question, Choice, QuizAttempt, Answer

class ChoiceInline(admin.TabularInline):
    """Inline admin for choices"""
    model = Choice
    extra = 4
    fields = ['choice_text', 'is_correct', 'order']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Question Admin with inline choices"""
    list_display = ['question_text_short', 'quiz', 'points', 'order', 'total_choices']
    list_filter = ['quiz__course', 'quiz', 'points']
    search_fields = ['question_text', 'quiz__title']
    ordering = ['quiz', 'order']
    
    inlines = [ChoiceInline]
    
    fieldsets = (
        ('Question Details', {
            'fields': ('quiz', 'question_text', 'explanation', 'points', 'order')
        }),
    )
    
    def question_text_short(self, obj):
        """Display shortened question text"""
        return obj.question_text[:100] + '...' if len(obj.question_text) > 100 else obj.question_text
    question_text_short.short_description = 'Question'
    
    def total_choices(self, obj):
        """Display total choices"""
        return obj.choices.count()
    total_choices.short_description = 'Choices'


class QuestionInline(admin.TabularInline):
    """Inline admin for questions"""
    model = Question
    extra = 0
    fields = ['question_text', 'points', 'order']
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Quiz Admin"""
    list_display = ['title', 'course', 'total_questions', 'total_points', 
                    'time_limit', 'passing_score', 'is_active', 'created_at']
    list_filter = ['course__category', 'course', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'course__title']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['course', 'order']
    
    inlines = [QuestionInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'title', 'slug', 'description')
        }),
        ('Quiz Settings', {
            'fields': ('time_limit', 'passing_score', 'max_attempts', 
                      'show_correct_answers', 'randomize_questions')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Choice Admin"""
    list_display = ['choice_text_short', 'question_short', 'is_correct_badge', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['choice_text', 'question__question_text']
    
    def choice_text_short(self, obj):
        """Display shortened choice text"""
        return obj.choice_text[:80] + '...' if len(obj.choice_text) > 80 else obj.choice_text
    choice_text_short.short_description = 'Choice'
    
    def question_short(self, obj):
        """Display shortened question"""
        return obj.question.question_text[:60] + '...' if len(obj.question.question_text) > 60 else obj.question.question_text
    question_short.short_description = 'Question'
    
    def is_correct_badge(self, obj):
        """Display colored badge for correct answer"""
        if obj.is_correct:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Correct</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px;">Incorrect</span>'
        )
    is_correct_badge.short_description = 'Status'


class AnswerInline(admin.TabularInline):
    """Inline admin for answers"""
    model = Answer
    extra = 0
    fields = ['question', 'selected_choice', 'is_correct']
    readonly_fields = ['question', 'selected_choice', 'is_correct']
    can_delete = False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Quiz Attempt Admin"""
    list_display = ['user', 'quiz', 'score_display', 'points_display', 
                    'passed_badge', 'time_taken_display', 'completed_at']
    list_filter = ['is_passed', 'quiz__course', 'quiz', 'started_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['user', 'quiz', 'score', 'points_earned', 'total_points', 
                      'is_passed', 'time_taken', 'started_at', 'completed_at']
    ordering = ['-started_at']
    
    inlines = [AnswerInline]
    
    fieldsets = (
        ('Attempt Information', {
            'fields': ('user', 'quiz', 'started_at', 'completed_at', 'time_taken')
        }),
        ('Results', {
            'fields': ('score', 'points_earned', 'total_points', 'is_passed')
        }),
    )
    
    def score_display(self, obj):
        """Display score with percentage"""
        return f"{obj.score}%"
    score_display.short_description = 'Score'
    
    def points_display(self, obj):
        """Display points earned/total"""
        return f"{obj.points_earned}/{obj.total_points}"
    points_display.short_description = 'Points'
    
    def passed_badge(self, obj):
        """Display pass/fail badge"""
        if obj.is_passed:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 3px;">PASSED</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 5px 10px; border-radius: 3px;">FAILED</span>'
        )
    passed_badge.short_description = 'Status'
    
    def time_taken_display(self, obj):
        """Display time taken in readable format"""
        minutes = obj.time_taken // 60
        seconds = obj.time_taken % 60
        return f"{minutes}m {seconds}s"
    time_taken_display.short_description = 'Time Taken'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Answer Admin"""
    list_display = ['user_name', 'question_short', 'selected_choice_short', 
                    'correct_badge', 'answered_at']
    list_filter = ['is_correct', 'attempt__quiz', 'answered_at']
    search_fields = ['attempt__user__username', 'question__question_text']
    readonly_fields = ['attempt', 'question', 'selected_choice', 'is_correct', 'answered_at']
    
    def user_name(self, obj):
        """Get username"""
        return obj.attempt.user.username
    user_name.short_description = 'User'
    
    def question_short(self, obj):
        """Display shortened question"""
        return obj.question.question_text[:60] + '...' if len(obj.question.question_text) > 60 else obj.question.question_text
    question_short.short_description = 'Question'
    
    def selected_choice_short(self, obj):
        """Display shortened selected choice"""
        return obj.selected_choice.choice_text[:50] + '...' if len(obj.selected_choice.choice_text) > 50 else obj.selected_choice.choice_text
    selected_choice_short.short_description = 'Selected Answer'
    
    def correct_badge(self, obj):
        """Display correct/incorrect badge"""
        if obj.is_correct:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">✓ Correct</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px;">✗ Wrong</span>'
        )
    correct_badge.short_description = 'Result'