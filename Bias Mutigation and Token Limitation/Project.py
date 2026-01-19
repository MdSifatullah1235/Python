import os
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def generate_respons(prompt,temperature=0.3):
    try:
        contents=[types.Content(role="user",parts=[types.Part.from_text(text=prompt)])]
        config_params=types.GenerateContentConfig(temperature=temperature)
        response=client.models.generate_content(
        model="gemini-2.0-flash",contents=contents,config=config_params)
        return response.text
    except Exception as e:
        return f"Error {str(e)}"
    
def bias_mitigation_activity():
    print("Bias mitigaton activity")

    prompt = input("Enter a prompt to explore bias: ")
    initial_response=generate_respons(prompt)
    print(f"initial Ai reponse: {initial_response}")

    modified_prompt=input("Modify the prompt to make it more neutral: ")
    modified_response=generate_respons(modified_prompt)
    print(f"modified ai response: {modified_response}")

def token_limit_activity():
    print("Token limit activity")

    long_prompt=input("Enter a long prompt: ")
    long_response=generate_respons(long_prompt)
    print(f"Response to long prompt: {long_response[:500]}")
    
    short_prompt=input("Now condense the prompt to be more consise: ")
    short_response=generate_respons(short_prompt)
    print(f"Response to condensed prompt: {short_prompt}")

def run_activyt():
    print("AI LEARNING ACTIVTY")
    activity_choose=input("Which activity would u like to run?(1: Bias, 2: token limits): ")
    if activity_choose=="1":
        bias_mitigation_activity()
    elif activity_choose=="2":
        token_limit_activity()
    else:
        print("Invalid choice please put 1 or 2")

if __name__=="__main__":
    run_activyt()