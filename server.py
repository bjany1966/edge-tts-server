from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import openai
import tempfile

app = FastAPI()

client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")

@app.post("/stt")
async def stt(file: UploadFile = File(...)):

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.write(await file.read())
    tmp.close()

    with open(tmp.name, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    return JSONResponse({"text": result.text})
