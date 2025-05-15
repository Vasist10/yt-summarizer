document.addEventListener('DOMContentLoaded', () => {
    const videoUrlInput = document.getElementById('videoUrl');
    const summarizeBtn = document.getElementById('summarizeBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const results = document.getElementById('results');
    const summary = document.getElementById('summary');
    const transcript = document.getElementById('transcript');
    const error = document.getElementById('error');

    summarizeBtn.addEventListener('click', async () => {
        const videoUrl = videoUrlInput.value.trim();
        
        if (!videoUrl) {
            showError('Please enter a YouTube video URL');
            return;
        }

        if (!isValidYouTubeUrl(videoUrl)) {
            showError('Please enter a valid YouTube URL');
            return;
        }

        try {
            // Show loading state
            loadingIndicator.classList.remove('hidden');
            results.classList.add('hidden');
            error.classList.add('hidden');
            summarizeBtn.disabled = true;

            console.log('Sending request to backend...');
            // Call backend API
            const response = await fetch('http://localhost:5000/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ videoUrl }),
            });

            console.log('Response status:', response.status);
            const data = await response.json();
            console.log('Received data:', data);

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to process video');
            }

            // Display results
            if (data.summary && data.transcript) {
                summary.textContent = data.summary;
                transcript.textContent = data.transcript;
                results.classList.remove('hidden');
                console.log('Results displayed successfully');
            } else {
                throw new Error('Invalid response format from server');
            }
        } catch (err) {
            console.error('Error:', err);
            showError(err.message || 'An error occurred while processing the video');
        } finally {
            loadingIndicator.classList.add('hidden');
            summarizeBtn.disabled = false;
            // Keep the URL in the input field
            videoUrlInput.value = videoUrl;
        }
    });

    function showError(message) {
        console.error('Showing error:', message);
        error.textContent = message;
        error.classList.remove('hidden');
        results.classList.add('hidden');
    }

    function isValidYouTubeUrl(url) {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/;
        return pattern.test(url);
    }
}); 