from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import edge_tts
import tempfile

app = FastAPI()

VOICE = "hu-HU-NoemiNeural"

@app.get("/tts")
async def tts(text: str):

    communicate = edge_tts.Communicate(text, VOICE)

    tmp = tempfile.SpooledTemporaryFile()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            tmp.write(chunk["data"])

    tmp.seek(0)

    return StreamingResponse(tmp, media_type="audio/mpeg")
