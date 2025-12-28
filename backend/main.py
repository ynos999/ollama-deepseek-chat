from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import json

app = FastAPI()

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

class Prompt(BaseModel):
    message: str

def stream_llm(prompt: str):
    payload = {
        "model": "deepseek-custom",
        "prompt": prompt,
        "stream": True
    }

    with requests.post(OLLAMA_URL, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                data = json.loads(line.decode())
                if "response" in data:
                    yield data["response"]

@app.post("/chat")
def chat(prompt: Prompt):
    return StreamingResponse(
        stream_llm(prompt.message),
        media_type="text/plain"
    )
