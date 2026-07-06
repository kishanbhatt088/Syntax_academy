from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Quiz, Question, Answer, QuizAttempt, Choice
from django.utils import timezone

@login_required
def quiz_list_view(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    quizzes = Quiz.objects.filter(course=course)
    
    context = {
        'course': course,
        'quizzes': quizzes,
    }
    return render(request, 'quiz/quiz_list.html', context)

@login_required
def quiz_detail_view(request, course_slug, quiz_id):
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, id=quiz_id, course=course)
    
    context = {
        'course': course,
        'quiz': quiz,
    }
    return render(request, 'quiz/quiz_detail.html', context)

@login_required
def take_quiz_view(request, course_slug, quiz_id):
    course = get_object_or_404(Course, slug=course_slug)
    quiz = get_object_or_404(Quiz, id=quiz_id, course=course)
    
    if request.method == 'POST':
        start_time = float(request.POST.get('start_time', timezone.now().timestamp()))
        time_taken = int(timezone.now().timestamp() - start_time)
        
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            time_taken=max(0, time_taken)
        )
        
        for question in quiz.questions.all():
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                try:
                    selected_choice = Choice.objects.get(id=choice_id, question=question)
                    Answer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_choice=selected_choice,
                    )
                except Choice.DoesNotExist:
                    pass
                    
        attempt.calculate_score()
        attempt.completed_at = timezone.now()
        attempt.save()
        
        # Trigger course progress recalculation
        try:
            from courses.models import Enrollment
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            enrollment.calculate_progress()
        except Enrollment.DoesNotExist:
            pass
        
        answer_details = []
        for answer in attempt.answers.all():
            correct_choice = answer.question.choices.filter(is_correct=True).first()
            answer_details.append({
                'question': answer.question,
                'selected_choice': answer.selected_choice,
                'is_correct': answer.is_correct,
                'correct_choice': correct_choice,
                'explanation': answer.question.explanation
            })
            
        context = {
            'title': f'Result: {quiz.title}',
            'course': course,
            'quiz': quiz,
            'attempt': attempt,
            'show_answers': quiz.show_correct_answers,
            'answer_details': answer_details
        }
        return render(request, 'quiz/quiz_result.html', context)
    
    # GET request
    start_time = timezone.now().timestamp()
    questions = quiz.questions.all()
    if quiz.randomize_questions:
        questions = questions.order_by('?')
        
    context = {
        'title': f'Take Quiz: {quiz.title}',
        'course': course,
        'quiz': quiz,
        'questions': questions,
        'start_time': start_time,
    }
    return render(request, 'quiz/quiz_take.html', context)