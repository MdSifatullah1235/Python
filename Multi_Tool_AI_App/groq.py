import Multi_Tool_AI_App.config as config
from openai import OpenAI

GROQ_URL = "https://groq.io/api/v1"
MODELS = getattr(config, "GROQ_MODELS", ["llama-3.1-8b-instant", "mixtral-7b-instruct-v0.2"])


def generate_response(prompt: str, temperature:float = 0.3, max_tokens = int = 512) -> str:
    key = getattr(config, "GROQ_API_KEY", None)
    if not key:
        return "API key not found"
    c = OpenAI(api_key=key, base_url=GROQ_URL)

    last_err = None

    for m in MODELS:
        try:
            r = c.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}], temperature=temperature, max_tokens=max_tokens)
            return r.choices[0].message.content
        
        except Exception as e:
            last_err = e
        
    
    return (
        "GROQ Model failed to respond. Error: " + str(last_err)
    )