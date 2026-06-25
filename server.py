from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@app.get("/")
def root():
    return {"status": "OK"}


@app.get("/ping")
def ping():
    return {"status": "alive"}


@app.post("/stt")
async def stt(request: Request):

    try:
        data = await request.json()
        text = data.get("text", "")

        print("USER:", text)
        print("KEY EXISTS:", bool(GEMINI_API_KEY))

        if not GEMINI_API_KEY:
            return {"error": "NO API KEY"}

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Válaszolj röviden magyarul: {text}"}
                    ]
                }
            ]
        }

        print("CALLING GEMINI...")

        try:
            r = requests.post(url, json=payload, timeout=15)
        except requests.exceptions.Timeout:
            return {"error": "Gemini timeout"}

        print("STATUS:", r.status_code)
        print("RAW:", r.text)

        if r.status_code != 200:
            return {
                "error": "Gemini HTTP error",
                "status": r.status_code,
                "raw": r.text
            }

        try:
            result = r.json()
        except Exception:
            return {
                "error": "Invalid JSON from Gemini",
                "raw": r.text
            }

        if "candidates" not in result:
            return {
                "error": "No candidates",
                "raw": result
            }

        answer = result["candidates"][0]["content"]["parts"][0]["text"]

        print("ANSWER:", answer)

        return {
            "text": text,
            "reply": answer
        }

    except Exception as e:
        print("🔥 SERVER ERROR:", repr(e))
        return {"error": str(e)}
