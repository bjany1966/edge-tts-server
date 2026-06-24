from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()

    print("Audio received:", len(audio))

    # 👉 ide jön majd Whisper / AI
    text = "szia"

    return {"text": text}
