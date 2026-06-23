from fastapi import FastAPI
from fastapi.responses import Response
import edge_tts
import io

app = FastAPI()

VOICE = "hu-HU-NoemiNeural"

@app.get("/tts")
async def tts(text: str):

    communicate = edge_tts.Communicate(text, VOICE)

    pcm = io.BytesIO()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            pcm.write(chunk["data"])

    return Response(
        content=pcm.getvalue(),
        media_type="application/octet-stream"
    )
