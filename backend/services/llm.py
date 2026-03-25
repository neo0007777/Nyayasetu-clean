import os
from groq import Groq
import ollama

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def call_groq(system_prompt: str, user_message: str) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
        max_tokens=2500,
    )
    return response.choices[0].message.content.strip()


def call_ollama(system_prompt: str, user_message: str) -> str:
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response["message"]["content"].strip()


def call_llm(system_prompt: str, user_message: str) -> str:
    groq_key = os.getenv("GROQ_API_KEY", "")
    use_groq = groq_key and groq_key != "your_groq_api_key_here"

    if use_groq:
        try:
            return call_groq(system_prompt, user_message)
        except Exception as e:
            print(f"[LLM] Groq failed: {e}. Switching to Ollama.")

    try:
        return call_ollama(system_prompt, user_message)
    except Exception as e:
        raise RuntimeError(
            f"[LLM] All providers failed. Make sure Ollama is running. Error: {e}"
        )
