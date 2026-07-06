# courses/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
import os
from .models import (
    Category, Course, Video, Note, Task, 
    UserVideoProgress, UserNoteProgress, UserTaskProgress, Enrollment
)
from .forms import TaskSubmissionForm


def category_list_view(request):
    categories = Category.objects.filter(is_active=True).annotate(
        course_count=Count('courses', filter=Q(courses__is_published=True))
    )
    return render(request, 'courses/category_list.html', {
        'categories': categories,
        'title': 'Categories'
    })


def course_list_view(request, category_slug=None):
    courses = Course.objects.filter(is_published=True).select_related('category')

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        courses = courses.filter(category=category)
        page_title = f'{category.name} Courses'
    else:
        page_title = 'All Courses'

    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Debug: Print count to terminal
    print(f"DEBUG: Found {courses.count()} courses")

    context = {
        'courses': courses,
        'category': category,
        'search_query': search_query,
        'title': page_title
    }
    return render(request, 'courses/course_list.html', context)


def course_detail_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    videos = course.videos.all().order_by('order')
    notes = course.notes.all().order_by('order')
    tasks = course.tasks.all().order_by('order')

    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            if enrollment.status == 'APPROVED':
                is_enrolled = True
        except Enrollment.DoesNotExist:
            pass

    task_progress = {}
    if request.user.is_authenticated:
        progress_records = UserTaskProgress.objects.filter(user=request.user, task__course=course)
        for record in progress_records:
            task_progress[record.task_id] = record

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'videos': videos,
        'notes': notes,
        'tasks': tasks,
        'task_progress': task_progress,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'title': course.title
    })


@login_required
def enroll_course_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, course=course
    )
    if created:
        messages.success(request, f'Enrollment request for {course.title} sent to admin for approval!')
    else:
        if enrollment.status == 'APPROVED':
            messages.info(request, f'Already enrolled in {course.title}.')
        elif enrollment.status == 'PENDING':
            messages.warning(request, f'Your enrollment request for {course.title} is still pending.')
        else:
            messages.error(request, f'Your enrollment request for {course.title} was rejected.')
            
    return redirect('courses:course_detail', slug=slug)


@login_required
def video_watch_view(request, course_slug, video_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    video = get_object_or_404(Video, course=course, slug=video_slug)

    if not video.is_preview:
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            if enrollment.status != 'APPROVED':
                if enrollment.status == 'PENDING':
                    messages.warning(request, 'Your enrollment is pending approval.')
                else:
                    messages.error(request, 'Your enrollment request was rejected.')
                return redirect('courses:course_detail', slug=course_slug)
        except Enrollment.DoesNotExist:
            messages.warning(request, 'Please enroll first.')
            return redirect('courses:course_detail', slug=course_slug)

    progress, created = UserVideoProgress.objects.get_or_create(
        user=request.user, video=video
    )
    all_videos = course.videos.all().order_by('order')

    return render(request, 'courses/video_watch.html', {
        'course': course,
        'video': video,
        'progress': progress,
        'all_videos': all_videos,
        'title': f'{video.title} - {course.title}'
    })


@login_required
def update_video_progress(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        progress, created = UserVideoProgress.objects.get_or_create(
            user=request.user, video=video
        )
        progress.watch_time = int(request.POST.get('watch_time', 0))
        progress.last_position = int(request.POST.get('last_position', 0))
        is_completed = request.POST.get('is_completed', 'false') == 'true'
        if is_completed and not progress.is_completed:
            progress.is_completed = True
            progress.completed_at = timezone.now()
        progress.save()
        
        # Trigger course progress recalculation
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=video.course, status='APPROVED')
            enrollment.calculate_progress()
        except Enrollment.DoesNotExist:
            pass
            
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def note_view(request, course_slug, note_slug):
    course = get_object_or_404(Course, slug=course_slug)
    note = get_object_or_404(Note, slug=note_slug, course=course)
    
    # THIS IS THE PROBLEM - it's a QuerySet
    # all_notes = Note.objects.filter(course=course).order_by('order')
    
    # FIX: Convert to a list
    all_notes = list(Note.objects.filter(course=course).order_by('order'))
    
    # Track progress
    progress, created = UserNoteProgress.objects.get_or_create(
        user=request.user, note=note
    )
    if not progress.is_read:
        progress.is_read = True
        progress.save()
        
        # Recalculate course progress
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course, status='APPROVED')
            enrollment.calculate_progress()
        except Enrollment.DoesNotExist:
            pass
    
    return render(request, 'courses/note_view.html', {
        'course': course,
        'note': note,
        'all_notes': all_notes,
    })


@login_required
def task_download_view(request, course_slug, task_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    task = get_object_or_404(Task, course=course, slug=task_slug)
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course)
        if enrollment.status != 'APPROVED':
            if enrollment.status == 'PENDING':
                messages.warning(request, 'Your enrollment is pending approval.')
            else:
                messages.error(request, 'Your enrollment request was rejected.')
            return redirect('courses:course_detail', slug=course_slug)
    except Enrollment.DoesNotExist:
        messages.warning(request, 'Please enroll first.')
        return redirect('courses:course_detail', slug=course_slug)
    if task.task_file:
        # We no longer mark as completed on download
        # Progress is only created if it doesn't exist
        UserTaskProgress.objects.get_or_create(
            user=request.user, task=task
        )

        import mimetypes
        content_type, encoding = mimetypes.guess_type(task.task_file.name)
        response = HttpResponse(task.task_file, content_type=content_type or 'application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(task.task_file.name)}"'
        return response
    messages.error(request, 'Task file not found.')
    return redirect('courses:course_detail', slug=course_slug)


@login_required
def task_submission_view(request, course_slug, task_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    task = get_object_or_404(Task, course=course, slug=task_slug)
    
    # Ensure user is enrolled
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course, status='APPROVED')
    except Enrollment.DoesNotExist:
        messages.warning(request, 'You must be an approved student to submit tasks.')
        return redirect('courses:course_detail', slug=course_slug)

    progress, created = UserTaskProgress.objects.get_or_create(
        user=request.user, task=task
    )

    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES, instance=progress)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.is_completed = True
            submission.completed_at = timezone.now()
            submission.save()
            
            # Recalculate course progress
            enrollment.calculate_progress()
            
            messages.success(request, f'Task "{task.title}" submitted successfully!')
        else:
            for error in form.errors.values():
                messages.error(request, error)
                
    return redirect('courses:course_detail', slug=course_slug)