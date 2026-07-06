# dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # User Dashboard
    path('', views.user_dashboard_view, name='home'),
    path('my-courses/', views.user_courses_view, name='user_courses'),
    path('my-progress/', views.user_progress_view, name='user_progress'),

    # Admin Dashboard
    path('admin/', views.admin_dashboard_view, name='admin'),
    path('admin/users/', views.admin_users_view, name='admin_users'),
    path('admin/enrollments/', views.admin_enrollments_view, name='admin_enrollments'),
    path('admin/user/<int:user_id>/', views.admin_user_detail_view, name='admin_user_detail'),

    # Admin Category Management
    path('admin/categories/', views.admin_category_list, name='admin_category_list'),
    path('admin/category/add/', views.admin_category_create, name='admin_category_create'),
    path('admin/category/<int:pk>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path('admin/category/<int:pk>/delete/', views.admin_category_delete, name='admin_category_delete'),

    # Admin Course Management
    path('admin/courses/', views.admin_course_list, name='admin_course_list'),
    path('admin/course/add/', views.admin_course_create, name='admin_course_create'),
    path('admin/course/<int:pk>/edit/', views.admin_course_edit, name='admin_course_edit'),
    path('admin/course/<int:pk>/delete/', views.admin_course_delete, name='admin_course_delete'),

    # Admin Video Management
    path('admin/course/<int:course_id>/videos/', views.admin_video_list, name='admin_video_list'),
    path('admin/course/<int:course_id>/video/add/', views.admin_video_create, name='admin_video_create'),
    path('admin/video/<int:pk>/edit/', views.admin_video_edit, name='admin_video_edit'),
    path('admin/video/<int:pk>/delete/', views.admin_video_delete, name='admin_video_delete'),

    # Admin Quiz Management
    path('admin/quizzes/', views.admin_quiz_list, name='admin_quiz_list'),
    path('admin/quiz/attempts/', views.admin_quiz_attempts_view, name='admin_quiz_attempts'),
    path('admin/quiz/<int:quiz_id>/questions/', views.admin_question_list, name='admin_question_list'),

    # Admin Q&A Management
    path('admin/qna/', views.admin_qna_list, name='admin_qna_list'),
    path('admin/qna/pending/', views.admin_qna_pending, name='admin_qna_pending'),

    # Admin Approval Flow
    path('admin/pending-requests/', views.admin_pending_requests_view, name='admin_pending_requests'),
    path('admin/user/<int:user_id>/approve/', views.admin_approve_user_view, name='admin_approve_user'),
    path('admin/user/<int:user_id>/reject/', views.admin_reject_user_view, name='admin_reject_user'),
    path('admin/enrollment/<int:enrollment_id>/approve/', views.admin_approve_enrollment_view, name='admin_approve_enrollment'),
    path('admin/enrollment/<int:enrollment_id>/reject/', views.admin_reject_enrollment_view, name='admin_reject_enrollment'),

    # Reports
    path('admin/reports/enrollments/csv/', views.admin_export_enrollments_csv, name='admin_export_enrollments_csv'),
    path('admin/reports/full-system/csv/', views.admin_export_full_system_csv, name='admin_export_full_system_csv'),
]