# courses/urls.py

from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('categories/', views.category_list_view, name='category_list'),
    path('courses/', views.course_list_view, name='course_list'),
    path('category/<slug:category_slug>/', views.course_list_view, name='course_by_category'),
    path('course/<slug:slug>/', views.course_detail_view, name='course_detail'),
    path('course/<slug:slug>/enroll/', views.enroll_course_view, name='enroll_course'),
    path('course/<slug:course_slug>/video/<slug:video_slug>/', views.video_watch_view, name='video_watch'),
    path('video/<int:video_id>/progress/', views.update_video_progress, name='update_video_progress'),
    path('course/<slug:course_slug>/note/<slug:note_slug>/', views.note_view, name='note_view'),
    path('course/<slug:course_slug>/task/<slug:task_slug>/download/', views.task_download_view, name='task_download'),
    path('course/<slug:course_slug>/task/<slug:task_slug>/submit/', views.task_submission_view, name='task_submission'),
]