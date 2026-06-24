from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/stt")
async def stt(file: UploadFile = File(...)):
    data = await file.read()
    return JSONResponse({"ok": True, "bytes": len(data)})
