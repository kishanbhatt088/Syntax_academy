# qna/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Question, Reply
from courses.models import Course, Enrollment


@login_required
def question_list_view(request):
    course_id = request.GET.get('course')
    status = request.GET.get('status')
    search = request.GET.get('search', '')

    if request.user.is_staff:
        questions = Question.objects.all()
    else:
        questions = Question.objects.filter(
            Q(is_public=True) | Q(user=request.user)
        )

    if course_id:
        questions = questions.filter(course_id=course_id)
    if status:
        questions = questions.filter(status=status)
    if search:
        questions = questions.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )

    questions = questions.select_related('user', 'course').annotate(
        reply_count=Count('replies')
    ).order_by('-created_at')

    paginator = Paginator(questions, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    if request.user.is_staff:
        courses = Course.objects.filter(is_published=True)
    else:
        enrolled_ids = Enrollment.objects.filter(
            user=request.user
        ).values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=enrolled_ids)

    context = {
        'page_obj': page_obj,
        'courses': courses,
        'selected_course': course_id,
        'selected_status': status,
        'search_query': search,
        'title': 'Q&A Forum'
    }
    return render(request, 'qna/question_list.html', context)


@login_required
def question_detail_view(request, pk):
    if request.user.is_staff:
        question = get_object_or_404(Question, pk=pk)
    else:
        question = get_object_or_404(
            Question.objects.filter(Q(is_public=True) | Q(user=request.user)),
            pk=pk
        )

    replies = question.replies.select_related('user').order_by('created_at')

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            is_solution = request.POST.get('is_solution') == 'on'
            Reply.objects.create(
                question=question,
                user=request.user,
                content=content,
                is_solution=is_solution if request.user.is_staff else False,
            )
            if request.user.is_staff and question.status == 'PENDING':
                question.status = 'ANSWERED'
                question.save()
            messages.success(request, 'Reply posted!')
            return redirect('qna:question_detail', pk=pk)
        else:
            messages.error(request, 'Reply cannot be empty.')

    context = {
        'question': question,
        'replies': replies,
        'title': question.title
    }
    return render(request, 'qna/question_detail.html', context)


@login_required
def question_create_view(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        is_public = request.POST.get('is_public') == 'on'

        if title and content and course_id:
            question = Question.objects.create(
                user=request.user,
                course_id=course_id,
                title=title,
                content=content,
                is_public=is_public,
                status='PENDING',
            )
            messages.success(request, 'Question posted!')
            return redirect('qna:question_detail', pk=question.pk)
        else:
            messages.error(request, 'All fields are required.')

    if request.user.is_staff:
        courses = Course.objects.filter(is_published=True)
    else:
        enrolled_ids = Enrollment.objects.filter(
            user=request.user
        ).values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=enrolled_ids)

    context = {
        'courses': courses,
        'title': 'Ask a Question',
        'action': 'Post Question'
    }
    return render(request, 'qna/question_form.html', context)


@login_required
def question_edit_view(request, pk):
    question = get_object_or_404(Question, pk=pk, user=request.user)

    if request.method == 'POST':
        question.title = request.POST.get('title', '').strip()
        question.content = request.POST.get('content', '').strip()
        question.course_id = request.POST.get('course')
        question.is_public = request.POST.get('is_public') == 'on'
        question.save()
        messages.success(request, 'Question updated!')
        return redirect('qna:question_detail', pk=pk)

    if request.user.is_staff:
        courses = Course.objects.filter(is_published=True)
    else:
        enrolled_ids = Enrollment.objects.filter(
            user=request.user
        ).values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=enrolled_ids)

    context = {
        'question': question,
        'courses': courses,
        'title': 'Edit Question',
        'action': 'Update Question'
    }
    return render(request, 'qna/question_form.html', context)


@login_required
def question_delete_view(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.user != question.user and not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('qna:question_list')

    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted!')
        return redirect('qna:question_list')

    return render(request, 'qna/question_confirm_delete.html', {
        'question': question,
        'title': 'Delete Question'
    })


@login_required
def my_questions_view(request):
    questions = Question.objects.filter(
        user=request.user
    ).select_related('course').annotate(
        reply_count=Count('replies')
    ).order_by('-created_at')

    paginator = Paginator(questions, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'qna/my_questions.html', {
        'page_obj': page_obj,
        'title': 'My Questions'
    })


@login_required
def reply_edit_view(request, pk):
    reply = get_object_or_404(Reply, pk=pk)

    if request.user != reply.user and not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('qna:question_detail', pk=reply.question.pk)

    if request.method == 'POST':
        reply.content = request.POST.get('content', '').strip()
        if request.user.is_staff:
            reply.is_solution = request.POST.get('is_solution') == 'on'
        reply.save()
        messages.success(request, 'Reply updated!')
        return redirect('qna:question_detail', pk=reply.question.pk)

    return render(request, 'qna/reply_form.html', {
        'reply': reply,
        'title': 'Edit Reply'
    })


@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, pk=pk)
    question_pk = reply.question.pk

    if request.user != reply.user and not request.user.is_staff:
        messages.error(request, 'Permission denied.')
        return redirect('qna:question_detail', pk=question_pk)

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted!')
        return redirect('qna:question_detail', pk=question_pk)

    return render(request, 'qna/reply_confirm_delete.html', {
        'reply': reply,
        'title': 'Delete Reply'
    })