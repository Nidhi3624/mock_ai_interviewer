# models.py
from django.db import models
from django.contrib.auth.models import User

class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_position = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    overall_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.job_position} Interview"

class Question(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.IntegerField()

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}..."

class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='answer')
    audio_file = models.FileField(upload_to='interview_answers/')
    transcription = models.TextField(blank=True)
    emotion_analysis = models.JSONField(default=dict)
    correctness_score = models.FloatField(default=0.0)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"Answer to: {self.question}"

class FacialAnalysis(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='facial_analyses')
    timestamp = models.FloatField()  # Timestamp within the video
    primary_emotion = models.CharField(max_length=20)
    emotion_details = models.JSONField()

    def __str__(self):
        return f"Facial Analysis at {self.timestamp}s"