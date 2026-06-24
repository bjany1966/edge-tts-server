import os
from openai import OpenAI

key = os.environ["OPENAI_API_KEY"].strip()
print(repr(key[:12]), len(key))

client = OpenAI(api_key=key)
print(client.models.list())
