from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.get("/")
def root():
    return {"status": "OK"}

@app.post("/stt")
async def stt(request: Request):

    data = await request.json()
    text = data.get("text", "")

    print("USER:", text)

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Válaszolj röviden magyarul: {text}"}
                    ]
                }
            ]
        }

        r = requests.post(url, json=payload, timeout=20)
        result = r.json()

        print("RAW:", result)

        answer = result["candidates"][0]["content"]["parts"][0]["text"]

        return {
            "text": text,
            "reply": answer
        }

    except Exception as e:
        print("ERROR:", repr(e))
        return {"error": str(e)}
