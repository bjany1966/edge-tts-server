from fastapi import FastAPI
from fastapi.responses import Response
import edge_tts
import io

app = FastAPI()

VOICE = "hu-HU-NoemiNeural"

@app.get("/tts")
async def tts(text: str):

    communicate = edge_tts.Communicate(text, VOICE)

    audio_data = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.write(chunk["data"])

    mp3 = audio_data.getvalue()

    return Response(
        content=mp3,
        media_type="audio/mpeg",
        headers={
            "Content-Length": str(len(mp3)),
            "Accept-Ranges": "bytes",
            "Connection": "close"
        }
    )
