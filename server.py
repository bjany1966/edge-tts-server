from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import wave
import openai
import os

app = FastAPI()
client = openai.OpenAI(api_key="sk_59414b9317ea7229b1f35a34ce35a72a109c5dd03b3a8b10")

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2

@app.post("/stt")
async def stt(request: Request):
    try:
        audio = await request.body()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            with wave.open(tmp, "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(SAMPLE_WIDTH)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(audio)
            wav_path = tmp.name

        with open(wav_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        os.unlink(wav_path)
        return JSONResponse({"text": result.text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
