from fastapi import FastAPI, Request
from openai import OpenAI
import tempfile

app = FastAPI()

client = OpenAI(api_key="sk_59414b9317ea7229b1f35a34ce35a72a109c5dd03b3a8b10")

@app.post("/stt")
async def stt(request: Request):

    try:
        audio = await request.body()
        print("Audio bytes:", len(audio))

        # 👉 csak mentés (FFMPEG nélkül!)
        f = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        f.write(audio)
        f.close()

        with open(f.name, "rb") as file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=file
            )

        return {"text": transcript.text}

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
