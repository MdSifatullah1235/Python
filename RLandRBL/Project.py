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

def reinforcement_learning_activity():
    prompt = input("Enter a prompt: ")
    initial_response = generate_response(prompt)
    print(f"\nInitial Response:\n{initial_response}\n")

    rating = input("Enter a rating (1-5): ")
    feedback = input("Enter feedback: ")

    improvement_prompt = f"The previous response was: '{initial_response}'. The user gave a rating of {rating}/5 and said: '{feedback}'. Please provide an improved version."
    improved_response = generate_response(improvement_prompt)

    print(f"\nImproved Response:\n{improved_response}\n")
    print("-" * 20)
    print("Reflection")
    print("1. What did you learn from the feedback?")
    print("2. How can I improve my responses in the future?")

def role_based_prompt_activity():
    category = input("Enter a category (e.g., Science): ")
    item = input("Enter a specific topic (e.g., Photosynthesis): ")

    teacher_prompt = f"You are a teacher. Explain the {category} of {item} in simple terms."
    expert_prompt = f"You are an expert in {category}. Explain {item} in technical detail."

    print(f"\nTeachers Perspective:\n{generate_response(teacher_prompt)}\n")
    print(f"\nExperts Perspective:\n{generate_response(expert_prompt)}\n")

    print("-" * 20)
    print("Reflection")
    print("1. How did the teacher and experts perspectives differ?")
    print("2. How can I improve my responses in the future?")

def run_activity():
    print("Select an Activity:")
    print("1. Reinforcement Learning Activity")
    print("2. Role-Based Prompt Activity")
    
    activity_choice = input("Enter the number: ")

    if activity_choice == "1":
        reinforcement_learning_activity()
    elif activity_choice == "2":
        role_based_prompt_activity()
    else:
        print("Invalid activity choice.")

if __name__ == "__main__":
    run_activity()