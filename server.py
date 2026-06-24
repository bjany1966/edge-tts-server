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
        print("Audio bytes:", len(audio))

        # 👉 valódi temp file kell
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        tmp.write(audio)
        tmp.close()

        with open(tmp.name, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        text = result.text
        print("USER:", text)

        return {"text": text}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
