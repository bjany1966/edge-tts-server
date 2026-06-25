@app.post("/stt")
async def stt(request: Request):
    audio = await request.body()
    print("Audio:", len(audio))
    return {"text": "ok"}
