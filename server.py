from fastapi import FastAPI, Request
import os
from openai import OpenAI
import tempfile

app = FastAPI()
client = OpenAI()

@app.get("/")
def root():
    return {"status": "OK"}

@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()

    print("STT HIT")
    print("Audio bytes:", len(audio))

    if len(audio) < 2000:
        return {"error": "too short audio"}

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.write(audio)
    tmp.close()

    # 🎤 1. WHISPER
    try:
        with open(tmp.name, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        user_text = transcript.text
        print("USER:", user_text)

    except Exception as e:
        print("WHISPER ERROR:", repr(e))
        return {"error": "whisper failed"}

    # 🤖 2. GPT
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Te egy segítőkész magyar hangasszisztens vagy."},
                {"role": "user", "content": user_text}
            ]
        )

        answer = response.choices[0].message.content
        print("GPT:", answer)

        return {
            "text": user_text,
            "reply": answer
        }

    except Exception as e:
        print("GPT ERROR:", repr(e))
        return {"error": "gpt failed"}
