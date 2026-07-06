from accounts.models import User
from courses.models import Enrollment
from qna.models import Question

def pending_requests_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        pending_users = User.objects.filter(is_staff=False, is_approved=False).count()
        pending_enrollments = Enrollment.objects.filter(status='PENDING').count()
        pending_questions = Question.objects.filter(status='PENDING').count()
        
        total_pending = pending_users + pending_enrollments
        
        return {
            'pending_users_count': pending_users,
            'pending_enrollments_count': pending_enrollments,
            'pending_questions_count': pending_questions,
            'total_pending_count': total_pending
        }
    return {
        'pending_users_count': 0,
        'pending_enrollments_count': 0,
        'pending_questions_count': 0,
        'total_pending_count': 0
    }
