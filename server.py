from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def root():
return {"version": "TEST_12345"}

@app.post("/stt")
async def stt(request: Request):

```
print("STT HIT")

audio = await request.body()

return {
    "bytes": len(audio),
    "version": "TEST_12345"
}
```
