from fastapi import FastAPI, Request
import os
from openai import OpenAI
import tempfile
import wave

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()
    print("STT HIT")
    print("Audio bytes:", len(audio))

    # safety check
    if len(audio) < 1000:
        return {"error": "too short audio"}

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

    # WAV wrapper
    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio)

    # Whisper
    with open(tmp.name, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    text = transcript.text
    print("USER:", text)

    return {
        "text": text
    }
