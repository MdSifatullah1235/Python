import streamlit as st
from groq import Groq
import requests
import json

st.set_page_config(page_title="CipherSolve Math AI", page_icon="🧮")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    .stChatMessage { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ App Settings")
    groq_api_key = st.text_input("Groq API Key", type="password")
    hf_api_key = st.text_input("Hugging Face API Key", type="password")
    
    st.divider()
    difficulty = st.select_slider(
        "Select Difficulty Level",
        options=["Elementary", "High School", "University", "Olympiad"]
    )
    
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()

    if st.button("📤 Export Session (JSON)"):
        chat_data = json.dumps(st.session_state.messages, indent=4)
        st.download_button("Download Transcript", chat_data, file_name="math_session.json")

st.title("🧮 CipherSolve Math Mastermind")
st.caption(f"Current Level: **{difficulty}** | Powered by Groq & Hugging Face")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

examples = ["Solve for x: 2x + 5 = 15", "What is the derivative of sin(x)?", "Calculate the area of a circle with radius 7."]
st.info(f"💡 Try: {examples[0]}")

def get_groq_response(prompt, level):
    client = Groq(api_key=groq_api_key)
    full_prompt = f"Level: {level}. Solve this math problem step-by-step: {prompt}"
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": full_prompt}]
    )
    return completion.choices[0].message.content

def get_hf_response(prompt, level):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {hf_api_key}"}
    payload = {"inputs": f"Math Level {level}: {prompt} Provide a step-by-step solution."}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()[0]['generated_text']

if user_input := st.chat_input("Enter your math problem here..."):
    if not groq_api_key or not hf_api_key:
        st.error("Please provide both API keys in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Calculating solutions..."):
            try:
                col1, col2 = st.columns(2)
                
                groq_ans = get_groq_response(user_input, difficulty)
                hf_ans = get_hf_response(user_input, difficulty)

                with col1:
                    st.subheader("Groq (Llama 3)")
                    st.write(groq_ans)
                
                with col2:
                    st.subheader("Hugging Face (Mistral)")
                    st.write(hf_ans)

                combined_response = f"**Groq:** {groq_ans}\n\n**Hugging Face:** {hf_ans}"
                st.session_state.messages.append({"role": "assistant", "content": combined_response})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")