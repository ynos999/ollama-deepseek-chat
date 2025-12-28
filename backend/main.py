from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests
import json
import os

app = FastAPI()

# Nolasa no Docker env, ja nav - izmanto tavu noklusējumu
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434/api/generate")

class Prompt(BaseModel):
    message: str

def stream_llm(prompt: str):
    payload = {
        "model": "deepseek-custom",
        "prompt": prompt,
        "stream": True
    }

    try:
        # Pievienojam timeout savienojuma izveidei, bet ne pašai datu saņemšanai
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=(5, None)) as r:
            r.raise_for_status() # Pārbauda, vai Ollama neatbild ar kļūdu
            for line in r.iter_lines():
                if line:
                    data = json.loads(line.decode())
                    if "response" in data:
                        yield data["response"]
    except Exception as e:
        yield f"\n[Kļūda savienojumā ar LLM: {str(e)}]"

@app.post("/chat")
async def chat(prompt: Prompt):
    return StreamingResponse(
        stream_llm(prompt.message),
        media_type="text/event-stream" # 'text/event-stream' ir labāks priekš Streaming
    )
