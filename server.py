from fastapi import FastAPI
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/test")
def test():

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input="Mondj egy szót magyarul."
        )

        return {"reply": response.output_text}

    except Exception as e:
        return {
            "type": type(e).__name__,
            "error": str(e)
        }
