import Multi_Tool_AI_App.config as config
from huggingface_hub import InferenceClient

MODELS = getattr(
    config,
    "HF_MODELS",
    ["meta-llama/Llama-3.1-8B-Instruct"] 
)

def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    key = getattr(config, "HF_API_KEY", None)
    if not key:
        return "Error: API key not found in config."
    
    last_err = None
    
    for model_id in MODELS:
        try:
            client = InferenceClient(model=model_id, token=key)
            response = client.chat_completion(
                messages=[{"role": "user", "content": prompt}], 
                temperature=temperature, 
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            last_err = e
            print(f"Model {model_id} failed: {e}")
            continue 

    return f"All Hugging Face models failed. Last error: {last_err}"