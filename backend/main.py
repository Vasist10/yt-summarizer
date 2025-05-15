from download_audio import download_audio
from transcribe import transcribe_audio
from summarize_hf import summarize_with_huggingface
from dotenv import load_dotenv
load_dotenv()

YOUTUBE_URL = "https://youtu.be/noJddjBQ51w?si=pQOezsiEkEgtCN77"  # replace this

download_audio(YOUTUBE_URL, "audio.mp3")
transcript = transcribe_audio("audio.mp3.mp3", translate=False)

# Write transcript to file
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(transcript)

# Read the transcript back
with open("transcript.txt", "r", encoding="utf-8") as f:
    full_transcript = f.read()

summary = summarize_with_huggingface(full_transcript)
with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)

print("\n📄 Summary written to summary.txt")
print("\n--- TRANSCRIPT ---\n")
print(transcript)
