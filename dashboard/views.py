# dashboard/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.utils.text import slugify
from datetime import timedelta
import csv

User = get_user_model()


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_staff:
            messages.error(request, 'Admin access only.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ==========================================
# USER VIEWS
# ==========================================

@login_required
def user_dashboard_view(request):
    from courses.models import Enrollment
    from quiz.models import QuizAttempt
    
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')[:5]
    quiz_attempts = QuizAttempt.objects.filter(user=request.user).select_related('quiz')[:5]
    
    context = {
        'enrollments': enrollments,
        'quiz_attempts': quiz_attempts,
        'title': 'My Dashboard'
    }
    return render(request, 'dashboard/user_dashboard.html', context)


@login_required
def user_courses_view(request):
    from courses.models import Enrollment
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'dashboard/user_courses.html', {'enrollments': enrollments, 'title': 'My Courses'})


@login_required
def user_progress_view(request):
    from courses.models import UserVideoProgress, UserNoteProgress, UserTaskProgress
    from quiz.models import QuizAttempt
    
    video_progress = UserVideoProgress.objects.filter(user=request.user).select_related('video', 'video__course')[:20]
    note_progress = UserNoteProgress.objects.filter(user=request.user).select_related('note', 'note__course')[:20]
    task_progress = UserTaskProgress.objects.filter(user=request.user).select_related('task', 'task__course')[:20]
    quiz_results = QuizAttempt.objects.filter(user=request.user).select_related('quiz')[:20]
    
    return render(request, 'dashboard/user_progress.html', {
        'video_progress': video_progress,
        'note_progress': note_progress,
        'task_progress': task_progress,
        'quiz_results': quiz_results,
        'title': 'My Progress'
    })


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@admin_required
def admin_dashboard_view(request):
    from courses.models import Category, Course, Video, Note, Task, Enrollment
    from quiz.models import Quiz, QuizAttempt
    from qna.models import Question
    
    stats = {
        'total_users': User.objects.filter(is_staff=False).count(),
        'new_users_month': User.objects.filter(
            is_staff=False, date_joined__gte=timezone.now() - timedelta(days=30)
        ).count(),
        'total_categories': Category.objects.count(),
        'total_courses': Course.objects.count(),
        'published_courses': Course.objects.filter(is_published=True).count(),
        'total_videos': Video.objects.count(),
        'total_notes': Note.objects.count(),
        'total_tasks': Task.objects.count(),
        'total_quizzes': Quiz.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'total_quiz_attempts': QuizAttempt.objects.count(),
        'avg_quiz_score': QuizAttempt.objects.aggregate(avg=Avg('score'))['avg'] or 0,
        'pending_questions': Question.objects.filter(status='PENDING').count(),
        'answered_questions': Question.objects.filter(status='ANSWERED').count(),
        'pending_users': User.objects.filter(is_staff=False, is_approved=False).count(),
        'pending_enrollments': Enrollment.objects.filter(status='PENDING').count(),
    }
    
    stats['total_pending'] = stats['pending_users'] + stats['pending_enrollments']
    
    recent_users = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
    recent_enrollments = Enrollment.objects.select_related('user', 'course').order_by('-enrolled_at')[:10]
    recent_questions = Question.objects.select_related('user', 'course').order_by('-created_at')[:10]
    popular_courses = Course.objects.filter(is_published=True).annotate(
        enrollment_count=Count('enrollments')
    ).order_by('-enrollment_count')[:5]
    
    return render(request, 'dashboard/admin_dashboard.html', {
        'stats': stats,
        'recent_users': recent_users,
        'recent_enrollments': recent_enrollments,
        'recent_questions': recent_questions,
        'popular_courses': popular_courses,
        'title': 'Admin Dashboard'
    })


# ==========================================
# ADMIN USERS
# ==========================================

@admin_required
def admin_users_view(request):
    search = request.GET.get('search', '')
    users = User.objects.filter(is_staff=False)
    if search:
        users = users.filter(Q(username__icontains=search) | Q(email__icontains=search))
    users = users.order_by('-date_joined')
    paginator = Paginator(users, 20)
    users = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/admin_users.html', {'users': users, 'search_query': search, 'title': 'Users'})


@admin_required
def admin_enrollments_view(request):
    from courses.models import Enrollment
    
    search = request.GET.get('search', '')
    course_id = request.GET.get('course_id')
    
    enrollments = Enrollment.objects.select_related('user', 'course')
    
    if search:
        enrollments = enrollments.filter(
            Q(user__username__icontains=search) | 
            Q(course__title__icontains=search)
        )
    
    if course_id:
        enrollments = enrollments.filter(course_id=course_id)
        
    enrollments = enrollments.order_by('-enrolled_at')
    
    paginator = Paginator(enrollments, 20)
    enrollments_page = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'dashboard/admin_enrollments.html', {
        'enrollments': enrollments_page,
        'search_query': search,
        'title': 'All Enrollments'
    })


@admin_required
def admin_user_detail_view(request, user_id):
    from courses.models import Enrollment
    from quiz.models import QuizAttempt
    
    profile_user = get_object_or_404(User, id=user_id)
    enrollments = Enrollment.objects.filter(user=profile_user).select_related('course')
    quiz_attempts = QuizAttempt.objects.filter(user=profile_user).select_related('quiz')[:10]
    
    return render(request, 'dashboard/admin_user_detail.html', {
        'profile_user': profile_user,
        'enrollments': enrollments,
        'quiz_attempts': quiz_attempts,
        'title': f'User: {profile_user.username}'
    })


# ==========================================
# ADMIN CATEGORIES
# ==========================================

@admin_required
def admin_category_list(request):
    from courses.models import Category
    categories = Category.objects.annotate(course_count=Count('courses')).order_by('order')
    return render(request, 'dashboard/admin_category_list.html', {'categories': categories, 'title': 'Categories'})


@admin_required
def admin_category_create(request):
    from courses.models import Category
    if request.method == 'POST':
        Category.objects.create(
            name=request.POST.get('name'),
            slug=request.POST.get('slug'),
            description=request.POST.get('description', ''),
            icon=request.POST.get('icon', 'fa-code'),
            color=request.POST.get('color', '#007bff'),
            order=request.POST.get('order', 0),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, 'Category created!')
        return redirect('dashboard:admin_category_list')
    return render(request, 'dashboard/admin_category_form.html', {'title': 'Add Category', 'action': 'Create'})


@admin_required
def admin_category_edit(request, pk):
    from courses.models import Category
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.slug = request.POST.get('slug')
        category.description = request.POST.get('description', '')
        category.icon = request.POST.get('icon', 'fa-code')
        category.color = request.POST.get('color', '#007bff')
        category.order = request.POST.get('order', 0)
        category.is_active = request.POST.get('is_active') == 'on'
        category.save()
        messages.success(request, 'Category updated!')
        return redirect('dashboard:admin_category_list')
    return render(request, 'dashboard/admin_category_form.html', {'category': category, 'title': 'Edit Category', 'action': 'Update'})


@admin_required
def admin_category_delete(request, pk):
    from courses.models import Category
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted!')
        return redirect('dashboard:admin_category_list')
    return render(request, 'dashboard/admin_category_confirm_delete.html', {'category': category})


# ==========================================
# ADMIN COURSES
# ==========================================

@admin_required
def admin_course_list(request):
    from courses.models import Course
    courses = Course.objects.select_related('category').annotate(
        video_count=Count('videos'), enrollment_count=Count('enrollments')
    ).order_by('-created_at')
    return render(request, 'dashboard/admin_course_list.html', {'courses': courses, 'title': 'Courses'})


@admin_required
def admin_course_create(request):
    from courses.models import Course, Category
    if request.method == 'POST':
        Course.objects.create(
            category_id=request.POST.get('category'),
            title=request.POST.get('title'),
            slug=request.POST.get('slug'),
            description=request.POST.get('description'),
            difficulty_level=request.POST.get('difficulty_level', 'BEGINNER'),
            estimated_duration=request.POST.get('estimated_duration', 0),
            prerequisites=request.POST.get('prerequisites', ''),
            learning_outcomes=request.POST.get('learning_outcomes', ''),
            is_published=request.POST.get('is_published') == 'on',
            created_by=request.user,
        )
        messages.success(request, 'Course created!')
        return redirect('dashboard:admin_course_list')
    categories = Category.objects.filter(is_active=True)
    return render(request, 'dashboard/admin_course_form.html', {'categories': categories, 'title': 'Add Course', 'action': 'Create'})


@admin_required
def admin_course_edit(request, pk):
    from courses.models import Course, Category
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.category_id = request.POST.get('category')
        course.title = request.POST.get('title')
        course.slug = request.POST.get('slug')
        course.description = request.POST.get('description')
        course.difficulty_level = request.POST.get('difficulty_level')
        course.estimated_duration = request.POST.get('estimated_duration', 0)
        course.prerequisites = request.POST.get('prerequisites', '')
        course.learning_outcomes = request.POST.get('learning_outcomes', '')
        course.is_published = request.POST.get('is_published') == 'on'
        course.save()
        messages.success(request, 'Course updated!')
        return redirect('dashboard:admin_course_list')
    categories = Category.objects.filter(is_active=True)
    return render(request, 'dashboard/admin_course_form.html', {'course': course, 'categories': categories, 'title': 'Edit Course', 'action': 'Update'})


@admin_required
def admin_course_delete(request, pk):
    from courses.models import Course
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted!')
        return redirect('dashboard:admin_course_list')
    return render(request, 'dashboard/admin_course_confirm_delete.html', {'course': course})


# ==========================================
# ADMIN VIDEOS
# ==========================================

@admin_required
def admin_video_list(request, course_id):
    from courses.models import Course
    course = get_object_or_404(Course, pk=course_id)
    videos = course.videos.all().order_by('order')
    return render(request, 'dashboard/admin_video_list.html', {'course': course, 'videos': videos, 'title': f'Videos - {course.title}'})


@admin_required
def admin_video_create(request, course_id):
    from courses.models import Course, Video
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        Video.objects.create(
            course=course,
            title=request.POST.get('title'),
            slug=slugify(request.POST.get('title')),
            description=request.POST.get('description', ''),
            video_url=request.POST.get('video_url', ''),
            duration=request.POST.get('duration', 0),
            order=request.POST.get('order', 0),
            is_preview=request.POST.get('is_preview') == 'on',
        )
        messages.success(request, 'Video added!')
        return redirect('dashboard:admin_video_list', course_id=course.id)
    return render(request, 'dashboard/admin_video_form.html', {'course': course, 'title': 'Add Video', 'action': 'Create'})


@admin_required
def admin_video_edit(request, pk):
    from courses.models import Video
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.title = request.POST.get('title')
        video.description = request.POST.get('description', '')
        video.video_url = request.POST.get('video_url', '')
        video.duration = request.POST.get('duration', 0)
        video.order = request.POST.get('order', 0)
        video.is_preview = request.POST.get('is_preview') == 'on'
        video.save()
        messages.success(request, 'Video updated!')
        return redirect('dashboard:admin_video_list', course_id=video.course.id)
    return render(request, 'dashboard/admin_video_form.html', {'video': video, 'title': 'Edit Video', 'action': 'Update'})


@admin_required
def admin_video_delete(request, pk):
    from courses.models import Video
    video = get_object_or_404(Video, pk=pk)
    course_id = video.course.id
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted!')
        return redirect('dashboard:admin_video_list', course_id=course_id)
    return render(request, 'dashboard/admin_video_confirm_delete.html', {'video': video})


# ==========================================
# ADMIN QUIZZES
# ==========================================

@admin_required
def admin_quiz_list(request):
    from quiz.models import Quiz
    quizzes = Quiz.objects.select_related('course').annotate(
        question_count=Count('questions'), attempt_count=Count('attempts')
    ).order_by('-created_at')
    return render(request, 'dashboard/admin_quiz_list.html', {'quizzes': quizzes, 'title': 'Quizzes'})


@admin_required
def admin_question_list(request, quiz_id):
    from quiz.models import Quiz
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all().prefetch_related('choices').order_by('order')
    return render(request, 'dashboard/admin_question_list.html', {'quiz': quiz, 'questions': questions, 'title': f'Questions - {quiz.title}'})


@admin_required
def admin_quiz_attempts_view(request):
    from quiz.models import QuizAttempt
    
    search = request.GET.get('search', '')
    quiz_id = request.GET.get('quiz_id')
    
    attempts = QuizAttempt.objects.select_related('user', 'quiz', 'quiz__course').annotate(
        attempted_questions=Count('answers')
    )
    
    if search:
        attempts = attempts.filter(
            Q(user__username__icontains=search) | 
            Q(quiz__title__icontains=search)
        )
    
    if quiz_id:
        attempts = attempts.filter(quiz_id=quiz_id)
        
    attempts = attempts.order_by('-started_at')
    
    paginator = Paginator(attempts, 20)
    attempts_page = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'dashboard/admin_quiz_attempts.html', {
        'attempts': attempts_page,
        'search_query': search,
        'title': 'Quiz Attempts'
    })


# ==========================================
# ADMIN Q&A
# ==========================================

@admin_required
def admin_qna_list(request):
    from qna.models import Question
    questions = Question.objects.select_related('user', 'course').annotate(
        reply_count=Count('replies')
    ).order_by('-created_at')
    paginator = Paginator(questions, 20)
    questions = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/admin_qna_list.html', {'questions': questions, 'title': 'Q&A'})


@admin_required
def admin_qna_pending(request):
    from qna.models import Question
    questions = Question.objects.filter(status='PENDING').select_related('user', 'course').order_by('-created_at')
    return render(request, 'dashboard/admin_qna_pending.html', {'questions': questions, 'title': 'Pending Questions'})


@admin_required
def admin_export_full_system_csv(request):
    from courses.models import Course, Video, Enrollment, UserVideoProgress
    from quiz.models import Quiz, QuizAttempt
    
    response = HttpResponse(content_type='text/csv')
    timestamp = timezone.now().strftime("%Y_%m_%d_%H%M%S")
    response['Content-Disposition'] = f'attachment; filename="syntax_full_report_{timestamp}.csv"'
    
    writer = csv.writer(response)
    
    # --- SECTION 1: SYSTEM SUMMARY ---
    writer.writerow(["### 1. SYSTEM SUMMARY ###"])
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total Registered Users", User.objects.filter(is_staff=False).count()])
    writer.writerow(["Active Users (Last 30 Days)", User.objects.filter(is_staff=False, last_login__gte=timezone.now() - timedelta(days=30)).count()])
    writer.writerow(["Total Courses", Course.objects.count()])
    writer.writerow(["Total Videos", Video.objects.count()])
    writer.writerow(["Total Quizzes", Quiz.objects.count()])
    writer.writerow(["Total Enrollments", Enrollment.objects.count()])
    writer.writerow([]) # Spacer
    
    # --- SECTION 2: USERS REPORT ---
    writer.writerow(["### 2. USERS REPORT ###"])
    writer.writerow(["User ID", "Name", "Email", "Status", "Last Active", "Enrolled Courses", "Completed Courses"])
    
    users = User.objects.filter(is_staff=False).prefetch_related('enrollments')
    for u in users:
        status = "Active" if u.last_login and u.last_login >= timezone.now() - timedelta(days=30) else "Inactive"
        enrolled_count = u.enrollments.count()
        completed_count = u.enrollments.filter(is_completed=True).count()
        writer.writerow([
            u.id, 
            u.get_full_name() or u.username, 
            u.email, 
            status, 
            u.last_login.strftime("%Y-%m-%d") if u.last_login else "Never",
            enrolled_count,
            completed_count
        ])
    writer.writerow([]) # Spacer
    
    # --- SECTION 3: COURSES REPORT ---
    writer.writerow(["### 3. COURSES REPORT ###"])
    writer.writerow(["Course ID", "Course Name", "Total Videos", "Total Quizzes", "Total Enrollments", "Completion Rate (%)"])
    
    courses = Course.objects.annotate(
        v_count=Count('videos', distinct=True),
        q_count=Count('quizzes', distinct=True),
        e_count=Count('enrollments', distinct=True)
    )
    for c in courses:
        completed_e = Enrollment.objects.filter(course=c, is_completed=True).count()
        completion_rate = round((completed_e / c.e_count * 100), 2) if c.e_count > 0 else 0
        writer.writerow([
            c.id, 
            c.title, 
            c.v_count, 
            c.q_count, 
            c.e_count, 
            f"{completion_rate}%"
        ])
    writer.writerow([]) # Spacer
    
    # --- SECTION 4: VIDEO ANALYTICS ---
    writer.writerow(["### 4. VIDEO ANALYTICS ###"])
    writer.writerow(["Video ID", "Course Name", "Video Title", "Total Views", "Avg Watch Time (Min)"])
    
    videos = Video.objects.select_related('course').annotate(
        view_count=Count('user_progress', distinct=True)
    )
    for v in videos:
        avg_seconds = UserVideoProgress.objects.filter(video=v).aggregate(avg=Avg('watch_time'))['avg'] or 0
        avg_minutes = round(avg_seconds / 60, 2)
        writer.writerow([
            v.id,
            v.course.title,
            v.title,
            v.view_count,
            avg_minutes
        ])
    writer.writerow([]) # Spacer
    
    # --- SECTION 5: QUIZ PERFORMANCE ---
    writer.writerow(["### 5. QUIZ PERFORMANCE ###"])
    writer.writerow(["Quiz ID", "Course Name", "Quiz Title", "Total Attempts", "Avg Score (%)", "Pass Rate (%)"])
    
    quizzes = Quiz.objects.select_related('course').annotate(
        attempt_count=Count('attempts', distinct=True)
    )
    for q in quizzes:
        avg_score = QuizAttempt.objects.filter(quiz=q).aggregate(avg=Avg('score'))['avg'] or 0
        pass_count = QuizAttempt.objects.filter(quiz=q, is_passed=True).count()
        pass_rate = round((pass_count / q.attempt_count * 100), 2) if q.attempt_count > 0 else 0
        writer.writerow([
            q.id,
            q.course.title,
            q.title,
            q.attempt_count,
            f"{round(avg_score, 2)}%",
            f"{pass_rate}%"
        ])
        
    return response


@admin_required
def admin_export_enrollments_csv(request):
    from courses.models import Enrollment
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="enrollments_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student Username', 'Student Email', 'Course', 'Enrollment Date', 'Progress %', 'Completed'])
    
    enrollments = Enrollment.objects.select_related('user', 'course').all().order_by('-enrolled_at')
    
    for enrollment in enrollments:
        writer.writerow([
            enrollment.user.username,
            enrollment.user.email,
            enrollment.course.title,
            enrollment.enrolled_at.strftime("%Y-%m-%d %H:%M"),
            enrollment.progress_percentage,
            'Yes' if enrollment.is_completed else 'No'
        ])
    
    return response


@admin_required
def admin_pending_requests_view(request):
    from courses.models import Enrollment
    
    pending_users = User.objects.filter(is_staff=False, is_approved=False).order_by('-date_joined')
    pending_enrollments = Enrollment.objects.filter(status='PENDING').select_related('user', 'course').order_by('-enrolled_at')
    
    return render(request, 'dashboard/admin_pending_requests.html', {
        'pending_users': pending_users,
        'pending_enrollments': pending_enrollments,
        'title': 'Pending Requests'
    })


@admin_required
def admin_approve_user_view(request, user_id):
    user_to_approve = get_object_or_404(User, id=user_id)
    user_to_approve.is_approved = True
    user_to_approve.save()
    messages.success(request, f'User {user_to_approve.username} approved successfully!')
    return redirect('dashboard:admin_pending_requests')


@admin_required
def admin_reject_user_view(request, user_id):
    user_to_reject = get_object_or_404(User, id=user_id)
    username = user_to_reject.username
    user_to_reject.delete()
    messages.warning(request, f'User {username} registration request rejected and account deleted.')
    return redirect('dashboard:admin_pending_requests')


@admin_required
def admin_approve_enrollment_view(request, enrollment_id):
    from courses.models import Enrollment
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    enrollment.status = 'APPROVED'
    enrollment.save()
    messages.success(request, f'Enrollment for {enrollment.user.username} in {enrollment.course.title} approved!')
    return redirect('dashboard:admin_pending_requests')


@admin_required
def admin_reject_enrollment_view(request, enrollment_id):
    from courses.models import Enrollment
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    enrollment.status = 'REJECTED'
    enrollment.save()
    messages.warning(request, f'Enrollment for {enrollment.user.username} in {enrollment.course.title} rejected.')
    return redirect('dashboard:admin_pending_requests')