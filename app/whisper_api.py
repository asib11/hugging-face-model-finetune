import os
import tempfile
import urllib.request
from pathlib import Path
from pydantic import BaseModel
from fastapi import APIRouter
from transformers import pipeline

router = APIRouter()


#STT --> speech to text model
MODEL_PATH = Path(__file__).resolve().parents[1] / "AIModels" / "whisper"
pipe = pipeline("automatic-speech-recognition", model=MODEL_PATH)

class TranscriptionRequest(BaseModel):
    audio_url: str

@router.post("/transcribe-whisper")
def transcribe(request: TranscriptionRequest):
    # Download the audio file from the provided URL
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        urllib.request.urlretrieve(request.audio_url, temp_audio_file.name)
        temp_audio_path = temp_audio_file.name

    #audio --> model --> output token --> text
    transcription_result = pipe(temp_audio_path, return_timestamps=True)

    # Clean up the temporary audio file
    os.remove(temp_audio_path)

    return {"transcription": transcription_result["text"]}