from django.contrib import admin
from .models import InterviewSession, Question, Answer, FacialAnalysis

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_position', 'difficulty_level', 'date_created', 'overall_score')
    search_fields = ('job_position', 'user__username')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('session', 'order', 'text')
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'correctness_score')
    search_fields = ('question__text',)

@admin.register(FacialAnalysis)
class FacialAnalysisAdmin(admin.ModelAdmin):
    list_display = ('answer', 'timestamp', 'primary_emotion')
    search_fields = ('primary_emotion',)