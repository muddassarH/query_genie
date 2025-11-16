import  requests
import openai
from fastapi import  HTTPException


# --- Ollama Integration ---
def query_ollama(prompt: str, model: str = "duckdb-nsql:latest"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Ollama error")
    return response.content

# --- Chatgpt Integration ---
def query_llm(api_key: str, prompt: str, use_chatgpt=False):
    if use_chatgpt:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message["content"]
    else:
        return query_ollama(prompt)
