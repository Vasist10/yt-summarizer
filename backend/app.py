from flask import Flask, render_template, request
from download_audio import download_audio
from transcribe import transcribe_audio
from summarize_hf import summarize_with_huggingface
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        try:
            # Step 1: Download audio
            download_audio(youtube_url, "audio.mp3")

            # Step 2: Transcribe audio
            transcript = transcribe_audio("audio.mp3.mp3", translate=False)

            # Step 3: Summarize using Hugging Face
            summary = summarize_with_huggingface(transcript)

        except Exception as e:
            summary = f"❌ Error: {str(e)}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
