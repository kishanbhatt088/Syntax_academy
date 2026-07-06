# qna/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from courses.models import Course

class Question(models.Model):
    """User Questions Model"""
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        ANSWERED = 'ANSWERED', _('Answered')
        CLOSED = 'CLOSED', _('Closed')
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('User')
    )
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('Course')
    )
    
    title = models.CharField(
        max_length=300,
        verbose_name=_('Question Title')
    )
    
    content = models.TextField(
        verbose_name=_('Question Content')
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Status')
    )
    
    is_public = models.BooleanField(
        default=True,
        help_text='Can other users see this question?',
        verbose_name=_('Is Public')
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
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title[:50]}"
    
    @property
    def total_replies(self):
        """Get total number of replies"""
        return self.replies.count()
    
    @property
    def has_admin_reply(self):
        """Check if admin has replied"""
        return self.replies.filter(user__role=User.Role.ADMIN).exists()


class Reply(models.Model):
    """Replies to Questions"""
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('Question')
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name=_('User')
    )
    
    content = models.TextField(
        verbose_name=_('Reply Content')
    )
    
    is_solution = models.BooleanField(
        default=False,
        help_text='Mark as the solution to the question',
        verbose_name=_('Is Solution')
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
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')
        ordering = ['created_at']
    
    def __str__(self):
        return f"Reply by {self.user.username} on {self.question.title[:30]}"
    
    def save(self, *args, **kwargs):
        """Update question status when reply is added"""
        super().save(*args, **kwargs)
        
        # Update question status if admin replied
        if self.user.role == User.Role.ADMIN and self.question.status == Question.Status.PENDING:
            self.question.status = Question.Status.ANSWERED
            self.question.save()