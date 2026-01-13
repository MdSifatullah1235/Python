import os
import time
from google import genai
from google.genai import types
import config

# Initialize client globally or inside functions
client = genai.Client(api_key=config.GEMINI_API_KEY)

def generate_response(prompt, temperature=0.5):
    try:
        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="text/plain"
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=generate_content_config,
        )
        return response.text
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_streaming_response(prompt, temperature=0.5):
    try:
        print("\nStreaming Response (Ctrl + C to stop):")
        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="text/plain"
        )

        # Use the stream method
        for chunk in client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=prompt,
            config=generate_content_config,
        ):
            print(chunk.text, end="", flush=True)
        print("\n") # New line after stream ends

    except Exception as e:
        print(f"\nError during streaming: {e}")

def temperature_prompt_activity():
    print("Welcome to Advanced Prompt Engineering")
    print("Today we will learn about temperature prompt activity\n")

    # --- Part 1 ---
    print("Part 1: Temperature Exploration")
    print("-" * 30)
    base_prompt = input("Enter a creative prompt: ")

    print("\nLow Temperature (0.1)")
    print(generate_response(base_prompt, temperature=0.1))
    
    time.sleep(1)

    print("\nMedium Temperature (0.5)")
    print(generate_response(base_prompt, temperature=0.5))

    time.sleep(1)

    print("\nHigh Temperature (0.9)")
    print(generate_response(base_prompt, temperature=0.9))

    # --- Part 2 ---
    print("\nPart 2: Instruction Based Prompt")
    topic = input("Enter a topic: ")

    instruction_list = [
        f"Summarize the key facts about the {topic} in 3-4 sentences.",
        f"Explain the {topic} as if I'm 10 years old",
        f"Write a pro/con list about the {topic}",
        f"Create a fiction headline about the {topic} from 2050"
    ]

    for i, instr in enumerate(instruction_list, 1):
        print(f"\nInstruction {i}: {instr}")
        response = generate_response(instr)
        print(response)
        time.sleep(1)

    # --- Part 3 ---
    print("\nPart 3: Creating your own instruction based prompt")
    custom_prompt = input("Enter a custom prompt: ")
    custom_temp = 0.7 # Default
    try:
        temp_input = input("Set the temperature (0.0 to 1.0): ")
        custom_temp = float(temp_input)
        if not (0 <= custom_temp <= 1):
            print("Temperature must be between 0 and 1. Defaulting to 0.7")
            custom_temp = 0.7
    except ValueError:
        print("Invalid Input. Defaulting to 0.7")

    print(generate_response(custom_prompt, temperature=custom_temp))

if __name__ == "__main__":
    temperature_prompt_activity()
    
    print("\n" + "="*30)
    choice = input("Would you like a streaming response? (y/n): ").lower()
    if choice == "y":
        streaming_prompt = input("Enter a prompt for streaming: ")
        generate_streaming_response(streaming_prompt, temperature=0.7)