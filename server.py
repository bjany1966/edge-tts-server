from fastapi import FastAPI, Request
import tempfile
import subprocess
import openai

app = FastAPI()

@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()

    wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(audio)
    wav.close()

    # Whisper
    with open(wav.name, "rb") as f:
        text = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    return {"text": text.text}
