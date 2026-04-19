import requests

def ask_llm(context: str, question: str):
    prompt = f"""You are a helpful assistant. Answer the question using ONLY the information provided in the context below. If the context does not contain enough information, say "I don't have enough information to answer that."

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    if not response.ok or "response" not in data:
        error = data.get("error", f"HTTP {response.status_code}")
        raise RuntimeError(f"Ollama error: {error}")

    return data["response"]