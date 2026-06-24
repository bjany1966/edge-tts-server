from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/stt")
async def stt(request: Request):
    audio = await request.body()
    print("Audio:", len(audio))

    return {
        "text": "teszt",
        "reply": "szia"
    }
