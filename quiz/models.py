# quiz/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from courses.models import Course

class Quiz(models.Model):
    """Quiz Model"""
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name=_('Course')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Quiz Title')
    )
    
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('URL Slug')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    
    time_limit = models.IntegerField(
        help_text='Time limit in minutes (0 = no limit)',
        default=0,
        verbose_name=_('Time Limit (minutes)')
    )
    
    passing_score = models.IntegerField(
        default=70,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Minimum percentage to pass',
        verbose_name=_('Passing Score (%)')
    )
    
    max_attempts = models.IntegerField(
        default=3,
        help_text='Maximum number of attempts (0 = unlimited)',
        verbose_name=_('Max Attempts')
    )
    
    show_correct_answers = models.BooleanField(
        default=True,
        help_text='Show correct answers after completion',
        verbose_name=_('Show Correct Answers')
    )
    
    randomize_questions = models.BooleanField(
        default=False,
        verbose_name=_('Randomize Questions')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active')
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name=_('Display Order')
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
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')
        ordering = ['course', 'order', 'title']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    @property
    def total_questions(self):
        """Get total number of questions"""
        return self.questions.count()
    
    @property
    def total_points(self):
        """Get total points available"""
        return self.questions.aggregate(
            total=models.Sum('points')
        )['total'] or 0


class Question(models.Model):
    """Quiz Question Model"""
    
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('Quiz')
    )
    
    question_text = models.TextField(
        verbose_name=_('Question Text')
    )
    
    explanation = models.TextField(
        blank=True,
        help_text='Explanation shown after answering',
        verbose_name=_('Explanation')
    )
    
    points = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_('Points')
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name=_('Display Order')
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
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ['quiz', 'order', 'id']
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


class Choice(models.Model):
    """Answer Choices for Questions"""
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name=_('Question')
    )
    
    choice_text = models.CharField(
        max_length=500,
        verbose_name=_('Choice Text')
    )
    
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_('Is Correct Answer')
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name=_('Display Order')
    )
    
    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')
        ordering = ['order']
    
    def __str__(self):
        return self.choice_text


class QuizAttempt(models.Model):
    """Track user quiz attempts"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        verbose_name=_('User')
    )
    
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name=_('Quiz')
    )
    
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Score (%)')
    )
    
    points_earned = models.IntegerField(
        default=0,
        verbose_name=_('Points Earned')
    )
    
    total_points = models.IntegerField(
        default=0,
        verbose_name=_('Total Points')
    )
    
    is_passed = models.BooleanField(
        default=False,
        verbose_name=_('Passed')
    )
    
    time_taken = models.IntegerField(
        help_text='Time taken in seconds',
        default=0,
        verbose_name=_('Time Taken (seconds)')
    )
    
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Started At')
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Completed At')
    )
    
    class Meta:
        verbose_name = _('Quiz Attempt')
        verbose_name_plural = _('Quiz Attempts')
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}%)"
    
    def calculate_score(self):
        """Calculate quiz score"""
        correct_answers = self.answers.filter(is_correct=True).count()
        total_questions = self.quiz.total_questions
        
        if total_questions > 0:
            self.score = (correct_answers / total_questions) * 100
            self.is_passed = self.score >= self.quiz.passing_score
        else:
            self.score = 0
            self.is_passed = False
        
        # Calculate points
        self.points_earned = self.answers.filter(is_correct=True).aggregate(
            total=models.Sum('question__points')
        )['total'] or 0
        self.total_points = self.quiz.total_points
        
        self.save()
        return self.score


class Answer(models.Model):
    """User's answers to quiz questions"""
    
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_('Quiz Attempt')
    )
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_('Question')
    )
    
    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        verbose_name=_('Selected Choice')
    )
    
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_('Is Correct')
    )
    
    answered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Answered At')
    )
    
    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.question_text[:50]}"
    
    def save(self, *args, **kwargs):
        """Auto-check if answer is correct"""
        self.is_correct = self.selected_choice.is_correct
        super().save(*args, **kwargs)