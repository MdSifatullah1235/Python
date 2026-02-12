import re
import streamlit as st
from io import BytesIO
from huggingface_hub import InferenceClient

HF_TOKEN = "your_huggingface_api_key_here" 
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"

WORDS = ["sex", "nude", "gun", "porn", "gore", "hate symbols", "nsfw"]
PATS = [re.compile(rf"\b{word}\b", re.IGNORECASE) for word in WORDS]


def is_safe(prompt: str):
    """Checks if the prompt contains forbidden keywords."""
    p_lower = prompt.lower()
    for word in WORDS:
        if word in p_lower:
            return False, f"Blocked keyword detected: {word}"
    for pat in PATS:
        if pat.search(prompt):
            return False, "Safety filter triggered."
    return True, ""

def get_client():
    return InferenceClient(model=MODEL_ID, token=HF_TOKEN)

def generate_img(prompt: str):
    """Handles the image generation request."""
    ok, reason = is_safe(prompt)
    if not ok:
        return None, reason
    
    client = get_client()
    try:
        image = client.text_to_image(
            prompt,
            negative_prompt="nsfw, low quality, blurry, distorted",
            width=512,
            height=512,
            num_inference_steps=30,
            guidance_scale=7.5,
        )
        
        buf = BytesIO()
        image.save(buf, format="PNG")
        return buf.getvalue(), None
    except Exception as e:
        return None, f"HF API Error: {str(e)}"


def main():
    st.set_page_config(page_title="Safe Gen AI", layout="centered", page_icon="🎨")
    
    st.title("🛡️ More Safe AI Image Generator")
    st.write("Enter a description to generate an image. High-risk keywords are blocked.")

    with st.form(key="image_gen_form"):
        user_prompt = st.text_area(
            "Image Description",
            height=120,
            placeholder="A serene landscape with mountains and a lake at sunset...",
        )
        submit = st.form_submit_button("Generate Image")

    if submit:
        if not user_prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating Image..."):
                img_bytes, error = generate_img(user_prompt.strip())
                
                if error:
                    st.error(error)
                if img_bytes:
                    st.session_state["generated_image"] = img_bytes
                    st.success("Generated successfully!")

    if "generated_image" in st.session_state:
        st.image(st.session_state["generated_image"], caption="Generated Result")
        st.download_button(
            label="Download Image",
            data=st.session_state["generated_image"],
            file_name="generated_ai_image.png",
            mime="image/png",
        )

if __name__ == "__main__":
    main()