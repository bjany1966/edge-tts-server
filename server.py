import os
from openai import OpenAI

key = os.environ["sk_59414b9317ea7229b1f35a34ce35a72a109c5dd03b3a8b10"].strip()
print(repr(key[:12]), len(key))

client = OpenAI(api_key=key)
print(client.models.list())
