from fastapi import FastAPI
from fastapi.responses import FileResponse
import edge_tts
import tempfile
import wave

app = FastAPI()

VOICE = "hu-HU-NoemiNeural"

@app.get("/tts")
async def tts(text: str):

    # ideiglenes wav fájl
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

    communicate = edge_tts.Communicate(text, VOICE, rate="+0%")

    pcm_data = bytearray()

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            pcm_data.extend(chunk["data"])

    # WAV fejléc + PCM
    with wave.open(tmp_file.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm_data)

    return FileResponse(
        tmp_file.name,
        media_type="audio/wav"
    )
