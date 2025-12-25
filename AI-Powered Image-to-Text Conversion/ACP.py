import requests
import io
from PIL import Image

API_TOKEN ='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'
API_URL_GPT2 = "https://api-inference.huggingface.co/models/gpt2"
API_URL_SD = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
API_URL_VIT = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def query_api(payload, url):
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

def query_image_api(payload, url):
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.content

def run_pipeline(user_prompt):
    text_resp = query_api({"inputs": user_prompt}, API_URL_GPT2)
    expanded_text = text_resp[0]['generated_text']
    
    image_bytes = query_image_api({"inputs": expanded_text}, API_URL_SD)
    image = Image.open(io.BytesIO(image_bytes))
    image.save("generated.png")
    
    with open("generated.png", "rb") as f:
        img_data = f.read()
    
    caption_resp = requests.post(API_URL_VIT, headers=HEADERS, data=img_data).json()
    caption = caption_resp[0]['generated_text']
    
    return expanded_text, caption

prompt = "A sunset over a mountain range"
expanded, final_caption = run_pipeline(prompt)

print(f"Expanded: {expanded}")
print(f"Caption: {final_caption}")