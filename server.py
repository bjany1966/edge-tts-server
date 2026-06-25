from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()

    print("STT HIT")
    print("Audio bytes:", len(audio))

    return {
        "status": "received",
        "bytes": len(audio)
    }
