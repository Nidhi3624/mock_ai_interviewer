#mock_interview_app > utils.py


import os
import random
from google.cloud import vision
from google.oauth2 import service_account

# Use environment variable for credentials
credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
if credentials_path:
    client = vision.ImageAnnotatorClient.from_service_account_file(credentials_path)
else:
    client = vision.ImageAnnotatorClient()


def generate_questions(job_position, difficulty_level):
    questions = [
        "Tell me about yourself.",
        f"Why are you interested in the {job_position} position?",
        "What are your greatest strengths?",
        "What do you consider to be your weaknesses?",
        "Where do you see yourself in 5 years?",
    ]
    
    if difficulty_level == 'medium':
        questions.extend([
            f"Can you describe a challenging situation you've faced in a previous {job_position} role?",
            "How do you handle stress and pressure?",
        ])
    elif difficulty_level == 'hard':
        questions.extend([
            "Describe a time when you had to deal with a difficult coworker or client.",
            "How do you stay updated with the latest trends and technologies in your field?",
            f"What's the most innovative project you've worked on related to {job_position}?",
        ])
    
    # Shuffle and return a subset of questions
    random.shuffle(questions)
    return questions[:5]  # Return 5 random questions

def analyze_facial_expression(image_file):
    """Analyze facial expression in an image using Google Cloud Vision API."""
    with open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform face detection
    response = client.face_detection(image=image)
    faces = response.face_annotations

    if not faces:
        return "No faces detected in the image."

    # We'll focus on the first detected face
    face = faces[0]

    # Analyze emotions
    emotions = {
        'joy': face.joy_likelihood,
        'sorrow': face.sorrow_likelihood,
        'anger': face.anger_likelihood,
        'surprise': face.surprise_likelihood,
    }

    # Convert likelihood to descriptive string
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
    emotions = {emotion: likelihood_name[likelihood] for emotion, likelihood in emotions.items()}

    # Determine the primary emotion
    primary_emotion = max(emotions, key=lambda x: likelihood_name.index(emotions[x]))

    return {
        'primary_emotion': primary_emotion,
        'emotion_details': emotions,
        'face_bounds': {
            'vertices': [{
                'x': vertex.x,
                'y': vertex.y
            } for vertex in face.bounding_poly.vertices]
        }
    }

def analyze_video_interview(video_frames):
    """Analyze facial expressions in multiple frames from a video interview."""
    results = []
    for frame in video_frames:
        result = analyze_facial_expression(frame)
        results.append(result)
    
    # Aggregate results
    emotion_counts = {emotion: 0 for emotion in ['joy', 'sorrow', 'anger', 'surprise']}
    for result in results:
        primary_emotion = result['primary_emotion']
        emotion_counts[primary_emotion] += 1
    
    dominant_emotion = max(emotion_counts, key=emotion_counts.get)
    
    return {
        'dominant_emotion': dominant_emotion,
        'emotion_breakdown': emotion_counts,
        'frame_by_frame': results
    }

# Note: The analyze_audio function is missing from the provided code.
# If you need it, you should implement it here.

def analyze_audio(audio_file_path):
    # This is a placeholder function. You should implement the actual audio analysis here.
    # For now, it returns a mock result
    return "Transcription of the audio", {"primary": "neutral", "confidence": 0.8}
