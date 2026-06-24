from fastapi import FastAPI, Request
import tempfile
import subprocess
import os
import edge_tts
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key="sk_59414b9317ea7229b1f35a34ce35a72a109c5dd03b3a8b10")  # 👈 ide írd

VOICE = "hu-HU-NoemiNeural"

# ---------------- STT / AI / TTS ----------------
@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()

    print("Audio received:", len(audio))

    # ===== 1. SAVE AUDIO =====
    wav_in = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav_in.write(audio)
    wav_in.close()

    # ===== 2. WHISPER (speech to text) =====
    with open(wav_in.name, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    user_text = transcript.text
    print("USER:", user_text)

    # ===== 3. CHATGPT =====
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Te egy magyarul beszélő segítő vagy."},
            {"role": "user", "content": user_text}
        ]
    )

    reply = response.choices[0].message.content
    print("AI:", reply)

    # ===== 4. TTS =====
    wav_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    communicate = edge_tts.Communicate(reply, VOICE)
    await communicate.save(wav_out.name)

    # ===== 5. RETURN TEXT + AUDIO PATH =====
    return {
        "text": user_text,
        "reply": reply,
        "audio": "/tts_audio"
    }


# ---------------- OPTIONAL AUDIO ENDPOINT ----------------
@app.get("/tts_audio")
def tts_audio():
    return {"info": "ide később streameljük az mp3-at"}
