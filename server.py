from fastapi import FastAPI
from fastapi.responses import FileResponse
import edge_tts
import tempfile
import wave
import asyncio

app = FastAPI()

VOICE = "hu-HU-NoemiNeural"

@app.get("/tts")
async def tts(text: str):

    communicate = edge_tts.Communicate(text, VOICE)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

    pcm = bytearray()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            pcm.extend(chunk["data"])

    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm)

    return FileResponse(
        tmp.name,
        media_type="audio/wav"
    )
