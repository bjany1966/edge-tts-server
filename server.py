from fastapi import FastAPI, Request
import os
import tempfile
from openai import OpenAI
import wave

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/stt")
async def stt(request: Request):

    try:
        audio = await request.body()
        print("Audio bytes:", len(audio))

        # 🔥 túl rövid hang kiszűrése
        if len(audio) < 2000:
            return {"error": "too short audio"}

        # 🔥 WAV csomagolás
        tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

        with wave.open(tmp_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)      # 16-bit
            wf.setframerate(16000)
            wf.writeframes(audio)

        # 🔥 Whisper hívás
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        text = result.text
        print("USER:", text)

        return {"text": text}

    except Exception as e:
        print("ERROR:", repr(e))
        return {"error": str(e)}
