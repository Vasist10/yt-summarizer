import whisper

def transcribe_audio(file_path, translate=False):
    model = whisper.load_model("base")  
    result = model.transcribe(file_path, task="translate" if translate else "transcribe")
    return result["text"]
