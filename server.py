from fastapi import FastAPI, Request
import wave

app = FastAPI()

@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()

    print("Bytes:", len(audio))

    with wave.open("test.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(audio)

    return {"saved": len(audio)}
