import streamlit as st
from google import genai
import re
import io
import PIL
from PIL import Image
from io import BytesIO
import base64
import mimetypes
from google.genai import types



client = genai.Client(api_key="AIzaSyDbXzhPPacvr53JfF-DcLCXQlu2qbxq1VM")

def is_prompt_safe(prompt:str) -> bool:
    forbidden_keywords = [
        "violence","sex","gun","weapon","blood","nude","sex","porn", "drugs", "hate","rascism", "terror", "bomb", "abuse","kill","death","sucide","self-harm","hate speech"
    ]

    pattern = re.compile("".join(forbidden_keywords), re.IGNORECASE)
    return not bool(pattern.search(prompt))


def generate_img(prompt:str):

    if not is_prompt_safe(prompt):
        return None,"Your prompt contains sensitive content. Please try again with a different prompt."
    

    try:
        model = "gemini-2.0-flash"

    
        content = [
            types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
        ] 


        generate_content_config = types.GenerateContentConfig(
            response_modalities=[
                "IMAGE", 'TEXT'
            ],
            response_mime_type= "text/plain",

        )

        for chunk in client.models.generate_content_stream(model=model, contents=content,config=generate_content_config):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue

            if (chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data):
                inline_data = chunk.candidates[0].content.parts[0].inline_data.data

                data_buffer = inline_data.data

                image = Image.open(BytesIO(data_buffer))

                return image, None
            elif chunk.text:
                continue
        return None, "No image generated"

    except Exception as e:
        return None, f"Error: {e}"
    

def main():
    st.set_page_config(page_title="Safe AI Image Generator", layout="centered")
    st.title("Safe AI Image Generator")
    st.write(
        "Enter a description to generate a image the prompt should have no forbidden keywords"
    )

    st.info("This app uses Gemini 2.0 to generate images")

    with st.form(key="image_gen_form"):
        prompt = st.text_area(
            "Image Desc",
            height= 120,
            placeholder="Describe the image you want to generate",
        )

        submit = st.form_submit_button("Generate Image")


        if submit:
            if not prompt.strip():
                st.warning("Please enter a prompt.")

            else:
                with st.spinner("Generateing Image..."):
                    image, error =  generate_img(prompt.strip())
                

                if error:
                    st.error(error)

                elif image:
                    st.image(image,caption="Generated Image")

                    st.session_state.generated_image = image
                
                else:
                    st.error("No image generated")



    if hasattr(st.session_state, "generated_image") and st.session_state.generated_image:
        buf = BytesIO()
        st.session_state.generated_image.save(buf, format="PNG")
        byte_im = buf.getvalue()


        st.download_button(
            label="Download Image",
            data=byte_im,
            file_name="generated_image.png",
            mime="image/png",
            help = "Download the generated image",
        )



if __name__ == "__main__":
    main()