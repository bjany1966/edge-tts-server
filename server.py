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

        # 🔥 WAV FILE KÉZI FELÉPÍTÉS
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)   # 16-bit
            wf.setframerate(16000)
            wf.writeframes(audio)

        with open(tmp.name, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        return {"text": result.text}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
