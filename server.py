from fastapi import FastAPI, Request
import os
from openai import OpenAI
import tempfile

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/stt")
async def stt(request: Request):

    try:
        audio = await request.body()
        print("STT HIT")
        print("Audio bytes:", len(audio))

        if len(audio) < 2000:
            return {"error": "too short audio"}

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp.write(audio)
        tmp.close()

        with open(tmp.name, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        return {"text": transcript.text}

    except Exception as e:
        print("WHISPER ERROR:", repr(e))
        return {"error": str(e)}
