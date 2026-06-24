from fastapi import FastAPI, Request
import os
from openai import OpenAI
import tempfile
import wave

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/stt")
async def stt(request: Request):

    try:
        audio = await request.body()
        print("Audio bytes:", len(audio))

        # 🔥 sanity check (EZ FONTOS)
        if len(audio) < 1000:
            return {"error": "too short audio"}

        tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

        # 🔥 FIXED WAV HEADER
        with wave.open(tmp_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)      # 16-bit
            wf.setframerate(16000)
            wf.writeframes(audio)

        with open(tmp_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        return {
            "text": transcript.text
        }

    except Exception as e:
        print("ERROR:", repr(e))
        return {"error": str(e)}
