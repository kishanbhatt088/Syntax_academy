from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('course/<slug:course_slug>/quizzes/', views.quiz_list_view, name='quiz_list'),
    path('course/<slug:course_slug>/quiz/<int:quiz_id>/', views.quiz_detail_view, name='quiz_detail'),
    path('course/<slug:course_slug>/quiz/<int:quiz_id>/take/', views.take_quiz_view, name='take_quiz'),
]