from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from download_audio import download_audio
from transcribe import transcribe_audio
from summarize_hf import summarize_with_huggingface
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI(title="YouTube Video Summarizer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the frontend directory
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

class VideoRequest(BaseModel):
    videoUrl: str

@app.get("/")
async def read_root():
    return FileResponse("../frontend/index.html")

@app.get("/styles.css")
async def get_styles():
    return FileResponse("../frontend/styles.css")

@app.get("/script.js")
async def get_script():
    return FileResponse("../frontend/script.js")

@app.post("/summarize")
async def summarize_video(request: VideoRequest):
    try:
        if not request.videoUrl:
            raise HTTPException(status_code=400, detail="No video URL provided")

        # Download and process the video
        download_audio(request.videoUrl, "audio.mp3")
        transcript = transcribe_audio("audio.mp3.mp3", translate=False)

        # Write transcript to file
        with open("transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript)

        # Read transcript and generate summary
        with open("transcript.txt", "r", encoding="utf-8") as f:
            full_transcript = f.read()

        summary = summarize_with_huggingface(full_transcript)
        with open("summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)

        return {
            "transcript": transcript,
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
