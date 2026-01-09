from google import genai
import config

client = genai.Client(config.API_KEY)

def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )


def silly_prompt(prompt):
    print("Welcome to Prompt Engineering")
    print("Today we will learn about context,clarity and specificity")
    print("Let's start by creating a vague prompt and slowly refine it")

    vague_prompt = input("Enter a vague prompt: ")

    print(f"Vague Prompt:{vague_prompt}")
    vague_response = generate_response(vague_prompt)
    print("AI's response to this vague prompt:")
    print(vague_response)

    specific_prompt = input("Enter a specific prompt: ")

    print(f"Specific prompt: {specific_prompt}")
    specific_response = generate_response(specific_prompt)
    print("AI's response to this specific prompt:")
    print(specific_response)


    print("Now let's add specificity and context to our prompt")

    contextually_specfic_prompt = input("Enter a contextually specific prompt: ")
    contextually_specfic_response = generate_response(contextually_specfic_prompt)
    print("AI's response to this contextually specific prompt:")
    print(contextually_specfic_response)

# Reflection
#How did the AI perform when we made the prompt more specific?
#How did the AI perform when we made the prompt more contextually specific?
#How did the AI perform when we made the prompt more contextually specific and clarifiied?

silly_prompt()