from fastapi import FastAPI, Request
from openai import OpenAI
import tempfile
import subprocess

app = FastAPI()

client = OpenAI(api_key="SK-YOUR_KEY")

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()
    print("Audio bytes:", len(audio))

    # 🔥 1. mentés RAW-ként
    raw_file = tempfile.NamedTemporaryFile(delete=False, suffix=".raw")
    raw_file.write(audio)
    raw_file.close()

    # 🔥 2. WAV konvertálás (ESP I2S → Whisper kompatibilis)
    wav_file = raw_file.name + ".wav"

    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "s16le",
        "-ar", "16000",
        "-ac", "1",
        "-i", raw_file.name,
        wav_file
    ])

    # 🔥 3. WHISPER
    with open(wav_file, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    text = transcript.text
    print("USER:", text)

    return {
        "text": text
    }
