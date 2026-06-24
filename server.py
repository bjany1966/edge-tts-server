from fastapi import FastAPI, Request
import os
from openai import OpenAI

app = FastAPI()

# 🔥 API KEY ENV-ből
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/stt")
async def stt(request: Request):

    try:
        audio = await request.body()
        print("Audio bytes:", len(audio))

        # 🔥 Whisper (STT)
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", audio)
        )

        text = result.text
        print("USER:", text)

        return {
            "text": text
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "error": str(e)
        }
