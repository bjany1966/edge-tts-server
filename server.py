from fastapi import FastAPI
from fastapi.responses import FileResponse
import edge_tts
import tempfile

app = FastAPI()

VOICE = "hu-HU-NoemiNeural"

@app.get("/tts")
async def tts(text: str):

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    communicate = edge_tts.Communicate(text, VOICE)

    await communicate.save(tmp.name)

    return FileResponse(
        tmp.name,
        media_type="audio/mpeg"
    )
