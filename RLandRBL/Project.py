import os
from  google import genai
from google.genai import types

import config 

client = genai.Client(api_key=config.GEMINI_API_KEY)

def generate_response(prompt,temprature=0.3):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temprature)

        response = client.models.generate_content(model="gemini-2.0-flash", contents=contents, config=config_params)

        return response.text
    
    except Exception as e:
        print(f"Error: {e}")



def reinforcement_learning_activity():
    prompt = input("Enter a prompt: ")
    initial_response = generate_response(prompt)
    print(f"Initial Response: {initial_response}")

    rating = input("Enter a rating (1-5): ")
    feedback = input("Enter feedback: ")

    improved_response = f"{initial_response} (Improved with your feedback:{feedback})"

    print(f"Improved Response: {improved_response}")


    print("Reflection")
    print("1. What did you learn from the feedback? ")
    print("2. How can I improve my responses in the future? ")



def role_based_prompt_activity():

    category = input("Enter a category: ")
    item = input("Enter a specific topic: ")

    teacher_prompt = f"You are a teacher. Explain the {category} of {item} in simple terms."
    expert_prompt = f"You are an expert in {category}. Explain the {item} in detail."

    print(f"Teachers Perspective: {generate_response(teacher_prompt)}")
    print(f"Experts Perspective: {generate_response(expert_prompt)}")


    print("Reflection")
    print("1. How did the teacher and experts perspectives differ? ")
    print("2. How can I improve my responses in the future? ")



def run_activity():
    activity_choice = input("Enter the number of the activity you want to run: ")

    if activity_choice == "1":
        reinforcement_learning_activity()
    elif activity_choice == "2":
        role_based_prompt_activity()
    else:
        print("Invalid activity choice.")

    

if __name__ == "__main__":
    run_activity()