# interview_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('start/', views.start_interview, name='start_interview'),
    path('conduct/<int:session_id>/', views.conduct_interview, name='conduct_interview'),
    path('submit-answer/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('submit-facial-analysis/<int:answer_id>/', views.submit_facial_analysis, name='submit_facial_analysis'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('analyze-frame/', views.analyze_interview_frame, name='analyze_frame'),
]