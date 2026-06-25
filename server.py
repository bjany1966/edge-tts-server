from fastapi import FastAPI, Request
import os
from openai import OpenAI
import tempfile

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    try:
        with open(tmp.name, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        text = result.text
        print("TRANSCRIPT:", text)
        print("KEY EXISTS:", bool(os.getenv("OPENAI_API_KEY")))
        print("KEY START:", os.getenv("OPENAI_API_KEY")[:8])
        print("KEY EXISTS:", os.getenv("OPENAI_API_KEY") is not None)
print("KEY START:", str(os.getenv("OPENAI_API_KEY"))[:10])

        return {"text": text}

    except Exception as e:
        print("WHISPER ERROR:", repr(e))
        return {"error": str(e)}
