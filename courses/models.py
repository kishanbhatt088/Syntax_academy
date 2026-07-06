# courses/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from accounts.models import User
import os

class Category(models.Model):
    """
    Course Categories (Python, Java, etc.)
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Category Name')
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_('URL Slug')
    )
    
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_('Description')
    )
    
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='FontAwesome icon class (e.g., fa-python)',
        verbose_name=_('Icon Class')
    )
    
    color = models.CharField(
        max_length=7,
        default='#007bff',
        help_text='Hex color code (e.g., #007bff)',
        verbose_name=_('Color Code')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active')
    )
    
    order = models.IntegerField(
        default=0,
        help_text='Display order (lower number = higher priority)',
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
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def total_courses(self):
        """Get total number of courses in this category"""
        return self.courses.filter(is_published=True).count()


class Course(models.Model):
    """
    Main Course Model
    """
    
    class DifficultyLevel(models.TextChoices):
        BEGINNER = 'BEGINNER', _('Beginner')
        INTERMEDIATE = 'INTERMEDIATE', _('Intermediate')
        ADVANCED = 'ADVANCED', _('Advanced')
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name=_('Category')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Course Title')
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_('URL Slug')
    )
    
    description = models.TextField(
        verbose_name=_('Description')
    )
    
    difficulty_level = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.BEGINNER,
        verbose_name=_('Difficulty Level')
    )
    
    thumbnail = models.ImageField(
        upload_to='course_thumbnails/',
        blank=True,
        null=True,
        verbose_name=_('Thumbnail')
    )
    
    estimated_duration = models.IntegerField(
        help_text='Estimated duration in hours',
        default=0,
        verbose_name=_('Estimated Duration (hours)')
    )
    
    prerequisites = models.TextField(
        blank=True,
        help_text='Prerequisites for this course',
        verbose_name=_('Prerequisites')
    )
    
    learning_outcomes = models.TextField(
        blank=True,
        help_text='What students will learn',
        verbose_name=_('Learning Outcomes')
    )
    
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published')
    )
    
    order = models.IntegerField(
        default=0,
        help_text='Display order within category',
        verbose_name=_('Display Order')
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_courses',
        verbose_name=_('Created By')
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
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ['category', 'order', 'title']
    
    def __str__(self):
        return f"{self.category.name} - {self.title}"
    
    @property
    def total_videos(self):
        """Get total number of videos"""
        return self.videos.count()
    
    @property
    def total_notes(self):
        """Get total number of notes"""
        return self.notes.count()
    
    @property
    def total_tasks(self):
        """Get total number of tasks"""
        return self.tasks.count()


class Video(models.Model):
    """
    Video Content Model
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name=_('Course')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Video Title')
    )
    
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('URL Slug')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    
    video_file = models.FileField(
        upload_to='videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'mkv'])],
        verbose_name=_('Video File')
    )
    
    video_url = models.URLField(
        blank=True,
        help_text='YouTube or Vimeo URL (optional, if not uploading file)',
        verbose_name=_('Video URL')
    )
    
    duration = models.IntegerField(
        help_text='Duration in minutes',
        default=0,
        verbose_name=_('Duration (minutes)')
    )
    
    thumbnail = models.ImageField(
        upload_to='video_thumbnails/',
        blank=True,
        null=True,
        verbose_name=_('Thumbnail')
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name=_('Display Order')
    )
    
    is_preview = models.BooleanField(
        default=False,
        help_text='Can be viewed without enrollment',
        verbose_name=_('Is Preview')
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
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
        ordering = ['course', 'order', 'title']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_video_source(self):
        """Get video source (file or URL)"""
        if self.video_file and self.video_file.name:
            return self.video_file.url
        return self.embed_url

    @property
    def embed_url(self):
        """Automatically converts regular YouTube links to embed format"""
        if not self.video_url:
            return ""
            
        url = self.video_url
        
        # Fix youtu.be/VIDEO_ID format
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
            
        # Fix youtube.com/watch?v=VIDEO_ID format
        elif 'youtube.com/watch' in url:
            import urllib.parse as urlparse
            parsed = urlparse.urlparse(url)
            video_id = urlparse.parse_qs(parsed.query).get('v')
            if video_id:
                return f"https://www.youtube.com/embed/{video_id[0]}"
                
        # Return as is if already an embed or vimeo URL
        return url


class Note(models.Model):
    """
    Course Notes/Documentation Model
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name=_('Course')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Note Title')
    )
    
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('URL Slug')
    )
    
    content = models.TextField(
        verbose_name=_('Content')
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
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')
        ordering = ['course', 'order', 'title']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Task(models.Model):
    """
    Programming Tasks/Assignments Model
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('Course')
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Task Title')
    )
    
    slug = models.SlugField(
        max_length=200,
        verbose_name=_('URL Slug')
    )
    
    description = models.TextField(
        verbose_name=_('Description')
    )
    
    task_file = models.FileField(
        upload_to='tasks/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])],
        verbose_name=_('Task File (PDF)')
    )
    
    difficulty = models.CharField(
        max_length=20,
        choices=Course.DifficultyLevel.choices,
        default=Course.DifficultyLevel.BEGINNER,
        verbose_name=_('Difficulty')
    )
    
    estimated_time = models.IntegerField(
        help_text='Estimated time to complete in hours',
        default=1,
        verbose_name=_('Estimated Time (hours)')
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
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['course', 'order', 'title']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class UserVideoProgress(models.Model):
    """
    Track user's video watching progress
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='video_progress',
        verbose_name=_('User')
    )
    
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='user_progress',
        verbose_name=_('Video')
    )
    
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_('Is Completed')
    )
    
    watch_time = models.IntegerField(
        default=0,
        help_text='Total watch time in seconds',
        verbose_name=_('Watch Time (seconds)')
    )
    
    last_position = models.IntegerField(
        default=0,
        help_text='Last watched position in seconds',
        verbose_name=_('Last Position (seconds)')
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Completed At')
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
        verbose_name = _('User Video Progress')
        verbose_name_plural = _('User Video Progress')
        unique_together = ['user', 'video']
    
    def __str__(self):
        return f"{self.user.username} - {self.video.title}"


class UserNoteProgress(models.Model):
    """
    Track user's note reading progress
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='note_progress',
        verbose_name=_('User')
    )
    
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='user_progress',
        verbose_name=_('Note')
    )
    
    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Is Read')
    )
    
    read_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Read At')
    )
    
    class Meta:
        verbose_name = _('User Note Progress')
        verbose_name_plural = _('User Note Progress')
        unique_together = ['user', 'note']
    
    def __str__(self):
        return f"{self.user.username} - {self.note.title}"


class UserTaskProgress(models.Model):
    """
    Track user's task performance progress
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='task_progress',
        verbose_name=_('User')
    )
    
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='user_progress',
        verbose_name=_('Task')
    )
    
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_('Is Completed')
    )
    
    submission_file = models.FileField(
        upload_to='task_submissions/',
        null=True,
        blank=True,
        verbose_name=_('Submission File')
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Completed At')
    )
    
    class Meta:
        verbose_name = _('User Task Progress')
        verbose_name_plural = _('User Task Progress')
        unique_together = ['user', 'task']
    
    def __str__(self):
        return f"{self.user.username} - {self.task.title}"


class Enrollment(models.Model):
    """
    Track user course enrollments
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name=_('User')
    )
    
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name=_('Course')
    )

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Status')
    )
    
    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Enrolled At')
    )
    
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_('Is Completed')
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Completed At')
    )
    
    progress_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name=_('Progress Percentage')
    )
    
    class Meta:
        verbose_name = _('Enrollment')
        verbose_name_plural = _('Enrollments')
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    def calculate_progress(self):
        """Calculate course completion progress across all content types"""
        from quiz.models import QuizAttempt
        
        # 1. Video Progress
        total_videos = self.course.videos.count()
        completed_videos = UserVideoProgress.objects.filter(
            user=self.user,
            video__course=self.course,
            is_completed=True
        ).count()
        
        # 2. Note Progress
        total_notes = self.course.notes.count()
        read_notes = UserNoteProgress.objects.filter(
            user=self.user,
            note__course=self.course,
            is_read=True
        ).count()
        
        # 3. Task Progress
        total_tasks = self.course.tasks.count()
        completed_tasks = UserTaskProgress.objects.filter(
            user=self.user,
            task__course=self.course,
            is_completed=True
        ).count()
        
        # 4. Quiz Progress
        total_quizzes = self.course.quizzes.count()
        passed_quizzes = 0
        if total_quizzes > 0:
            # A quiz is considered "completed" if the user has a passing attempt
            quizzes = self.course.quizzes.all()
            for quiz in quizzes:
                if QuizAttempt.objects.filter(user=self.user, quiz=quiz, is_passed=True).exists():
                    passed_quizzes += 1
        
        # Calculate overall percentage
        total_items = total_videos + total_notes + total_tasks + total_quizzes
        
        if total_items == 0:
            self.progress_percentage = 100.00 if self.is_completed else 0.00
        else:
            completed_items = completed_videos + read_notes + completed_tasks + passed_quizzes
            progress = (completed_items / total_items) * 100
            self.progress_percentage = round(progress, 2)
        
        # Auto-mark course as completed if 100%
        if self.progress_percentage >= 100 and not self.is_completed:
            self.is_completed = True
            from django.utils import timezone
            self.completed_at = timezone.now()
            
        self.save()
        return self.progress_percentage