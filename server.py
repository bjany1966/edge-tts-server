from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import tempfile
import openai

app = FastAPI()
client = openai.OpenAI(api_key="YOUR_KEY")

@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".raw")
    tmp.write(audio)
    tmp.close()

    with open(tmp.name, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    return JSONResponse({"text": result.text})
