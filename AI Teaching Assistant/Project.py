import streamlit as st
from google import genai
from google.genai import types
from config import GEMINI_apikey
client = genai.Client(api_key=GEMINI_apikey)
def generate_response(prompt,temperature=0.3):
    try:
        contents=[types.Content(role="user",parts={types.Part.from_text(text=prompt)})]
        config_params=types.GenerateContentConfig(temperature=temperature)
        response=client.models.generate_content(model="gemini-2.0-flash",contents=contents,config=config_params)
        return response.text
    except Exception as e:
        return f"Error{str(e)}"
    
def setup_ui():
    st.title("Ai teaching assistant")
    st.write("Welcome you can ask me anything about various subjects and i will provide an answer")
    user_input=st.text_input("Enter your question here: ")
    if user_input:
        st.write(f"Your questions: {user_input}")
        response=generate_response(user_input)
        st.write(f"Answer: {response}")
    else:
        st.write("Please enter a question to ask")

def main():
    setup_ui()

if __name__=="__main__":
    main()