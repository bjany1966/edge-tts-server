import os
from openai import OpenAI

key = os.environ["OPENAI_API_KEY"].strip()
print(repr(key[:12]), len(key))
print("KEY PREFIX:", repr(os.getenv("OPENAI_API_KEY", "")[:10]))

client = OpenAI(api_key=key)
print(client.models.list())
