import config
from google import genai
from google.genai import types

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
        return response.text if response.text else "No response generated."
    except Exception as e:
        return f"Error: {e}"

logs_list = {}
counter = 0

while True:
    prompt = input("\nEnter a prompt (or type 'quit' to exit): ")
    if prompt.lower() == 'quit':
        break

    initial_response = generate_response(prompt)
    print(f"\nInitial Response:\n{initial_response}\n")

    rating = input("Enter a rating (1-5): ")
    feedback = input("Enter feedback: ")

    improvement_prompt = f"The previous response was: '{initial_response}'. User rating: {rating}/5. Feedback: '{feedback}'. Please improve it."
    improved_response = generate_response(improvement_prompt)

    print(f"\nImproved Response:\n{improved_response}\n")

    counter += 1
    logs_list[counter] = {
        "prompt": prompt,
        "improved": improved_response
    }

    view_logs = input("Do you want to see the logs list? (yes/no): ")
    if view_logs.lower() == "yes":
        for idx, entry in logs_list.items():
            print(f"Log #{idx}: {entry['improved'][:50]}...")