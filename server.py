from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import tempfile
import wave
import openai

app = FastAPI()
client = openai.OpenAI(api_key="YOUR_KEY")

SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit

@app.post("/stt")
async def stt(request: Request):
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

    return JSONResponse({"text": result.text})
