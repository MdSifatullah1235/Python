import os
from google.genai import types
from google import genai
import config


client = genai.Client(api_key=config.GEMINI_API_KEY)


def generate_response(prompt,temperature=0.3):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(prompt)])]

        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=config_params
        )
        return response.text

    except Exception as e:
        return f"Error: {e}"
    


def bias_mutigation_activity():
    prompt = input("Enter a prompt: (Eg, descrive the ideal doctor)")
    initial_response = generate_response(prompt)

    print(f"Initial AI Response: {initial_response}")


    modified_prompt = input("Enter a modified prompt: (Eg, describe the quailities of a doctor)")
    modified_response = generate_response(modified_prompt)

    print(f"Modified AI Response: {modified_response}")


def token_limit_activity():
    long_prompt = input("Enter a long prompt: (Eg, a story)")
    long_response = generate_response(long_prompt)
    print(f"Long Prompt Response: {long_response}")



    short_prompt = input("Enter a short prompt: (Eg, a sentence)")
    short_response = generate_response(short_prompt)
    print(f"Short Prompt Response: {short_response}")



def run_activity():
    activity_choice = input("Enter the number: ")

    if activity_choice == "1":
        bias_mutigation_activity()
    elif activity_choice == "2":
        token_limit_activity()
    else:
        print("Invalid activity choice.")

if __name__ == "__main__":
    run_activity()