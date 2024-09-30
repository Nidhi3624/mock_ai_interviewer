from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import InterviewSession, Question, Answer, FacialAnalysis
from .utils import generate_questions, analyze_audio, analyze_facial_expression
import os
from django.conf import settings

@login_required
def dashboard(request):
    sessions = InterviewSession.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'interview_app/dashboard.html', {'sessions': sessions})

@login_required
def start_interview(request):
    if request.method == 'POST':
        job_position = request.POST['job_position']
        difficulty_level = request.POST['difficulty_level']
        session = InterviewSession.objects.create(
            user=request.user,
            job_position=job_position,
            difficulty_level=difficulty_level
        )
        questions = generate_questions(job_position, difficulty_level)
        for i, q in enumerate(questions, 1):
            Question.objects.create(session=session, text=q, order=i)
        return redirect('conduct_interview', session_id=session.id)
    return render(request, 'interview_app/start_interview.html')

@login_required
def conduct_interview(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    questions = session.questions.all().order_by('order')
    return render(request, 'interview_app/conduct_interview.html', {'session': session, 'questions': questions})

@login_required
@csrf_exempt
def submit_answer(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)
        audio_file = request.FILES['audio']
        answer = Answer.objects.create(question=question, audio_file=audio_file)
        
        # Process the audio file
        audio_path = answer.audio_file.path
        transcription, emotion_analysis = analyze_audio(audio_path)
        answer.transcription = transcription
        answer.emotion_analysis = emotion_analysis
        answer.save()
        
        return JsonResponse({'status': 'success', 'answer_id': answer.id})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@csrf_exempt
def submit_facial_analysis(request, answer_id):
    if request.method == 'POST':
        answer = get_object_or_404(Answer, id=answer_id)
        timestamp = float(request.POST['timestamp'])
        image_file = request.FILES['image']
        
        # Save the image temporarily
        path = default_storage.save(f'tmp/facial_analysis_{answer_id}_{timestamp}.jpg', ContentFile(image_file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        
        facial_analysis = analyze_facial_expression(tmp_file)
        FacialAnalysis.objects.create(
            answer=answer,
            timestamp=timestamp,
            primary_emotion=facial_analysis['primary_emotion'],
            emotion_details=facial_analysis['emotion_details']
        )
        
        # Delete the temporary file
        default_storage.delete(tmp_file)
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    questions = session.questions.all().order_by('order')
    return render(request, 'interview_app/session_detail.html', {'session': session, 'questions': questions})

@login_required
@csrf_exempt
def analyze_interview_frame(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Save the image temporarily
        path = default_storage.save('tmp/interview_frame.jpg', ContentFile(image_file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        
        # Analyze the image
        result = analyze_facial_expression(tmp_file)
        
        # Delete the temporary file
        default_storage.delete(tmp_file)
        
        return JsonResponse(result)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)