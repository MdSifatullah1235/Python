import streamlit as st
from google import genai
from google.genai import types
import config2
import io



client = genai.Client(api_key=config2.GEMINI_apikey)

def generate_response(prompt, temperature=0.3):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature, max_output_tokens=600)
        response = client.models.generate_content(model="gemini-2.0-flash", contents=contents, config=config_params)


        return response.text

    except Exception as e:
        print("Error: ",e)

    

def setup_ui():
    st.set_page_config(page_title="AI Teaching Assistant Wiht Conversation History", layout="centered")

    st.title("🎓 AI Teaching Assistant")

    st.write("Ask me **anything**")

    if "history" not in st.session_state:
        st.session_state.history = []

    
    col_clear, col_export = st.columns([1,2])

    with col_clear:
        if st.button("Clear Conversation"):

            st.session_state.history = []
            st.experimental_rerun()
    
    with col_export:
        if st.session_state.history:
            export_text = ""
            for idx, qa  in enumerate(st.session_state.history, start=1):
                export_text += f"Q{idx}: {qa["question"]}\n"
                export_text += f"A{idx}: {qa['answer']}\n\n"
            

            bio = io.BytesIO()
            bio.write(export_text.encode('utf-8'))

            bio.seek(0)

            st.download_button(
                label="Download Conversation History",
                data=bio,
                file_name="conversation_history.txt",
                mime="text/plain"
            )

    user_input = st.text_input("Ask a question")


    if st.button("Ask"):
        if user_input.strip():
            with st.spinner("Generating AI Response")

                response = generate_response(user_input)

                st.session_state.history.append({"question": user_input, "answer": response})

                st.experimental_rerun()

            
        else:
            st.warning("Please enter a question")

    

    st.markdown("---")
    st.markdown(
        """
        <style>
            .history_box{
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ccc;
                padding: 12px;
                background-color: #f9f9f9;
                border-radius: 6px;
                font-family: monospace;
            }


            .question {
                font-weight: 600;
                color: #0072C6;
                margin-top: 12px;
                margin-bottom: 4px;
            }

            .answer{
                margin-bottom: 12px;
                white-space: pre-wrap;
                color: #333;
            }
        </style>
        """,

        unsafe_allow_html=True

    )



    history_html = "<div class=""history_box"">"

    for idx, qa in enumerate(st.session_state.history, start=1):
        q = qa["question"]
        a = qa["answer"]

        history_html += f"<div class=""question"">Q{idx}: {q}</div>"
        history_html += f"<div class=""answer"">A{idx}: {a}</div>"
    
    history_html += "<div/>"
    st.markdown(history_html, unsafe_allow_html=True)


def main():
    setup_ui()


if __name__ == "__main__":
    main()