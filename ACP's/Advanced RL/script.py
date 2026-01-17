import os
from google import genai
from google.genai import types
import config 

client = genai.Client(api_key=config.GEMINI_API_KEY)

def generate_response(prompt, temperature=0.3):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)

        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=contents, 
            config=config_params
        )

        return response.text if response.text else "No response generated (possibly filtered)."
    
    except Exception as e:
        return f"Error: {e}"

while True:
    def reinforcement_learning_activity():
        prompt = input("Enter a prompt: ")
        initial_response = generate_response(prompt)
        print(f"\nInitial Response:\n{initial_response}\n")

        rating = input("Enter a rating (1-5): ")
        feedback = input("Enter feedback: ")

        improvement_prompt = f"The previous response was: '{initial_response}'. The user gave a rating of {rating}/5 and said: '{feedback}'. Please provide an improved version."
        improved_response = generate_response(improvement_prompt)

        print(f"\nImproved Response:\n{improved_response}\n")

if __name__ == "__main__":
    reinforcement_learning_activity()