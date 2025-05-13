from flask import Flask, render_template, request
from download_audio import download_audio
from transcribe import transcribe_audio
from summarize_hf import summarize_with_huggingface
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        if youtube_url:
            try:
                # Step 1: Download audio
                audio_path = "audio.mp3"
                download_audio(youtube_url, audio_path)

                # Step 2: Transcribe audio
                transcript = transcribe_audio(audio_path, translate=False)

                # Optional: Save transcript
                with open("transcript.txt", "w", encoding="utf-8") as f:
                    f.write(transcript)

                # Step 3: Summarize using Hugging Face
                summary = summarize_with_huggingface(transcript)

                # Optional: Save summary
                with open("summary.txt", "w", encoding="utf-8") as f:
                    f.write(summary)

            except Exception as e:
                summary = f"❌ Error processing video: {str(e)}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
