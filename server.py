from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/stt")
async def stt(request: Request):

    audio = await request.body()
    print("Audio bytes:", len(audio))

    # 👉 most még FIX válasz (teszt stabilitás)
    text = "szia"

    return {
        "text": text
    }
