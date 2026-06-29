"""
Consumer example — the Tipsoi-flavored Gemini.

Identical to normal google-genai usage, with ONE change: point the client at
your proxy via http_options(base_url=...). The api_key is the access key you
were given (starts with tsg_), NOT a Google key.

    pip install google-genai
"""

import os
from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.environ.get("TIPSOI_KEY", "tsg_YOUR_ACCESS_KEY"),
    http_options=types.HttpOptions(
        base_url=os.environ.get("TIPSOI_BASE_URL", "https://tipsoi-gemini.onrender.com"),
    ),
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How do I apply for leave in Tipsoi?",
)
print(response.text)

# Streaming works the same way:
# for chunk in client.models.generate_content_stream(
#     model="gemini-2.5-flash", contents="ডিভাইস ডাটা আসছে না, কী করব?"):
#     print(chunk.text, end="")
