from fastapi import FastAPI
from fastapi.responses import Response
import edge_tts
import tempfile
import subprocess

app = FastAPI()

VOICE = "hu-HU-NoemiNeural"

@app.get("/tts")
async def tts(text: str):

    wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    pcm_file = tempfile.NamedTemporaryFile(delete=False, suffix=".raw")

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(wav_file.name)

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", wav_file.name,
        "-f", "s16le",
        "-ar", "16000",
        "-ac", "1",
        pcm_file.name
    ])

    data = open(pcm_file.name, "rb").read()

    return Response(content=data, media_type="application/octet-stream")
