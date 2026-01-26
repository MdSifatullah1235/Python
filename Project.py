import streamlit as st
from google import genai
from google.genai import types
from config import GEMINI_apikey

# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client(api_key=GEMINI_apikey)

def generate_response(prompt, history, temperature=0.3):
    try:
        contents = []

        # Add chat history
        for msg in history:
            contents.append(
                types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        # Add current user prompt
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            )
        )

        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=600
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=config
        )

        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="AI Teaching Assistant",
    page_icon="🎓"
)

st.title("🎓 AI Teaching Assistant")
st.write("Ask questions on **Maths, Science, Programming, History, or any subject**.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask your question...")

if user_input:
    # Show user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = generate_response(
                user_input,
                st.session_state.chat_history
            )
            st.markdown(answer)

    # Save AI message
    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )