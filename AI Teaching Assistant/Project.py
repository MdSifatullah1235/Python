import streamlit as st

from google import genai
from google.genai import types
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)



def generate_response(prompt,temperature=0.3):
    try:
        contents=[types.Content(role="user",parts=[types.Part.from_text(text=prompt)])]
        config_params=types.GenerateContentConfig(temperature=temperature)
        response=client.models.generate_content(model="gemini-2.0-flash",contents=contents,config=config_params)
        return response.text
    except Exception as e:
        return f"Error {str(e)}"


def setup_ui():
    st.title("AI Teaching Assistant")
    st.write("You can ask me about any subject, topic or anything in general")

    user_input = st.text_input("Enter your question: ")

    if user_input:
        st.write("Your question: ", user_input)

        response = generate_response(user_input)
        st.write("AI's response: ", response)

    else:
        st.write("Please enter a question.")


def main():
    setup_ui()


if __name__ == "__main__":
    main()