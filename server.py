import os
import tempfile
import wave
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI

app = FastAPI()

def get_client():
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")
    return OpenAI(api_key=key)

@app.get("/")
def root():
    return {"ok": True}

@app.post("/stt")
async def stt(request: Request):
    try:
        audio = await request.body()
        if not audio:
            raise HTTPException(status_code=400, detail="empty audio")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            with wave.open(tmp, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio)
            wav_path = tmp.name

        client = get_client()
        with open(wav_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        return JSONResponse({"text": result.text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
