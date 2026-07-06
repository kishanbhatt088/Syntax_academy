# qna/urls.py

from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path('', views.question_list_view, name='question_list'),
    path('question/<int:pk>/', views.question_detail_view, name='question_detail'),
    path('question/create/', views.question_create_view, name='question_create'),
    path('question/<int:pk>/edit/', views.question_edit_view, name='question_edit'),
    path('question/<int:pk>/delete/', views.question_delete_view, name='question_delete'),
    path('my-questions/', views.my_questions_view, name='my_questions'),
    path('reply/<int:pk>/edit/', views.reply_edit_view, name='reply_edit'),
    path('reply/<int:pk>/delete/', views.reply_delete_view, name='reply_delete'),
]