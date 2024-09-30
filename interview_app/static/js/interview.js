let mediaRecorder;
let audioChunks = [];

// Start Recording Function
function startRecording(questionId) {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];

                // Create FormData and send the audio to the server
                const formData = new FormData();
                formData.append('audio', audioBlob, `answer_${questionId}.wav`);
                
                // Submit the answer using AJAX
                fetch(`/submit_answer/${questionId}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        console.log('Answer submitted successfully:', data.answer_id);
                        // Optionally update the UI to reflect the submitted answer
                    } else {
                        console.error('Error submitting answer:', data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            };

            // Show stop recording button and hide start recording button
            document.getElementById(`question-${questionId}`).querySelector('.btn-danger').style.display = 'inline';
            document.getElementById(`question-${questionId}`).querySelector('.btn-primary').style.display = 'none';
        });
}

// Stop Recording Function
function stopRecording(questionId) {
    mediaRecorder.stop();

    // Hide stop recording button and show start recording button
    document.getElementById(`question-${questionId}`).querySelector('.btn-danger').style.display = 'none';
    document.getElementById(`question-${questionId}`).querySelector('.btn-primary').style.display = 'inline';
}

// Helper function to get CSRF token (if needed)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
