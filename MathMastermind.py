import streamlit as sl
from google.genai import types
from google import genai
import io

client = genai.Client(api_key="AIzaSyDbXzhPPacvr53JfF-DcLCXQlu2qbxq1VM")

def generate_response(prompt: str, temperature: float = 0.1) -> str:
    try:
        system_prompt = (
            "You are a math mastermind. Follow this structure for every response:\n"
            "1. Problem Statement\n"
            "2. Problem Categorization (e.g., Algebra, Calculus)\n"
            "3. Step-by-Step Analysis & Solution\n"
            "4. Conclusion & Final Answer\n"
            "5. Brief Summary\n"
            "6. References/Concepts used."
        )
        
        full_prompt = f"{system_prompt} \n\n Math problem: {prompt}"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=1000
            )
        )

        return response.text
    
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    sl.set_page_config(page_title="AI Teaching Assistant", layout="centered")

    sl.title("🧮 Math Mastermind")
    sl.write("Ask me **anything** about mathematics.")

    with sl.expander("Example problems I can solve:"):
        sl.markdown(
            "- **Algebra:** Solve quadratic equations or systems of equations.\n"
            "- **Calculus:** Find derivatives, integrals, or limits.\n"
            "- **Statistics:** Calculate mean, variance, and standard deviation.\n"
            "- **Geometry:** Area/Volume calculations and geometric proofs."
        )

    if "history" not in sl.session_state:
        sl.session_state.history = []
    
    if "input_key" not in sl.session_state:
        sl.session_state.input_key = 0

    col_clear, col_export = sl.columns([1, 2])
    with col_clear:
        if sl.button("Clear Conversation"):
            sl.session_state.history = []
            sl.rerun()
    
    with col_export:
        if sl.session_state.history:
            export_text = ""
            for idx, qa in enumerate(sl.session_state.history, start=1):
                export_text += f"Q{idx}: {qa['question']}\n"
                export_text += f"A{idx}: {qa['answer']}\n\n"

            sl.download_button(
                label="Download History",
                data=export_text,
                file_name="math_history.txt",
                mime="text/plain"
            )

    with sl.form(key="my_form", clear_on_submit=True):
        user_input = sl.text_area(
            "Enter your problem here:",
            height=100,
            placeholder="Example: Solve for x: 2x + 10 = 20",
        )

        col1, col2 = sl.columns([3, 1])

        with col1:
            submitted = sl.form_submit_button("Submit")

        with col2:
            difficulty = sl.selectbox("Difficulty", ["Basic", "Intermediate", "Advanced"]) 
            
    if submitted:
        if user_input.strip():
            enhanced_prompt = f"Difficulty: {difficulty} | Problem: {user_input}"
            with sl.spinner("Solving..."):
                response = generate_response(enhanced_prompt)
            
            sl.session_state.history.insert(0, {"question": user_input, "answer": response})
            sl.rerun()
        else:
            sl.error("Please enter a valid problem.")

    # History Display
    if sl.session_state.history:
        sl.divider()
        sl.subheader("Solution History")

        sl.markdown("""
            <style>
            .history-item {
                background-color: #f0f2f6;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
                border-left: 5px solid #ff4b4b;
            }
            .question-text { font-weight: bold; color: #1f77b4; }
            .answer-text { white-space: pre-wrap; margin-top: 10px; }
            </style>
        """, unsafe_allow_html=True)

        for h in sl.session_state.history:
            sl.markdown(f"""
                <div class="history-item">
                    <div class="question-text">Q: {h['question']}</div>
                    <div class="answer-text">{h['answer']}</div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()