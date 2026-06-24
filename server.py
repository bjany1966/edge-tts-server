import os
import tempfile
import wave
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.environ["sk_59414b9317ea7229b1f35a34ce35a72a109c5dd03b3a8b10"].strip())

@app.post("/stt")
async def stt(request: Request):
    try:
        audio = await request.body()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            with wave.open(tmp, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio)
            wav_path = tmp.name

        with open(wav_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        return JSONResponse({"text": result.text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
