from google import genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text 

def silly_prompt():
    print("Welcome to Prompt Engineering")
    print("Today we will learn about context, clarity, and specificity\n")

    vague_prompt = input("Enter a vague prompt (e.g., 'Write a story'): ")
    vague_response = generate_response(vague_prompt)
    print(f"\nAI's response to: {vague_prompt}")
    print(vague_response)
    print("-" * 30)

    specific_prompt = input("Enter a specific prompt (e.g., 'Write a 2-sentence story about a cat'): ")
    specific_response = generate_response(specific_prompt)
    print(f"\nAI's response to: {specific_prompt}")
    print(specific_response)
    print("-" * 30)

    context_prompt = input("Enter a contextually specific prompt: ")
    context_response = generate_response(context_prompt)
    print(f"\nAI's response to: {context_prompt}")
    print(context_response)

if __name__ == "__main__":
    silly_prompt()