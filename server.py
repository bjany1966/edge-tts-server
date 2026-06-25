from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# 🔑 API KEY (Render ENV-ből jön)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@app.get("/")
def root():
    return {"status": "OK"}


@app.post("/stt")
async def stt(request: Request):

    try:
        data = await request.json()
        text = data.get("text", "")

        print("USER:", text)
        print("KEY:", GEMINI_API_KEY)

        if not GEMINI_API_KEY:
            return {"error": "NO API KEY SET"}

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

        print("BEFORE GEMINI")

        try:
            r = requests.post(
                url,
                json=payload,
                timeout=10,
                headers={"Content-Type": "application/json"}
            )
        except requests.exceptions.Timeout:
            return {"error": "Gemini timeout"}

        print("AFTER GEMINI")
        print("STATUS:", r.status_code)
        print("RAW:", r.text)

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

        return {
            "text": text,
            "reply": answer
        }

    except Exception as e:
        print("🔥 HARD ERROR:", repr(e))
        return {"error": str(e)}
