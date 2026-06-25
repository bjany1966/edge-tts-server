from fastapi import FastAPI, Request
from google import genai
import os

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def root():
    return {"status": "OK"}

@app.post("/stt")
async def stt(request: Request):

    data = await request.json()
    text = data.get("text", "")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=text
        )

        return {
            "text": text,
            "reply": response.text
        }
        print("KEY LENGTH:", len(GEMINI_API_KEY))
        print("RESPONSE OBJ:", response)
        print("TEXT:", response.text)

    except Exception as e:
        return {"error": str(e)}
