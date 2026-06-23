from fastapi import FastAPI
from fastapi.responses import FileResponse
import edge_tts
import tempfile
import asyncio

app = FastAPI()

VOICE = "hu-HU-NoemiNeural"

@app.get("/tts")
async def tts(text: str):

    communicate = edge_tts.Communicate(text, VOICE)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            tmp_file.write(chunk["data"])

    tmp_file.close()

    return FileResponse(
        tmp_file.name,
        media_type="audio/mpeg",
        filename="tts.mp3"
    )
