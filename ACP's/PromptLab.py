import google as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def get_response(prompt, temp):
    config = genai.types.GenerationConfig(temperature=temp)
    response = model.generate_content(prompt, generation_config=config)
    return response.text

print("--- Part 1: Temperature Testing ---")
creative_prompt = "Describe a city on Mars"
for t in [0.1, 0.5, 0.9]:
    print(f"\nTemperature: {t}")
    print(get_response(creative_prompt, t))

print("\n--- Part 2: Instruction-Based Prompt Testing ---")
topic = "climate change"
instructions = [
    f"Provide a summary of {topic}",
    f"Give a simplified explanation of {topic}",
    f"Create a pro-con list regarding {topic} solutions",
    f"Write a creative headline from the future about {topic}"
]
for prompt in instructions:
    print(f"\nInstruction: {prompt}")
    print(get_response(prompt, 0.7))

print("\n--- Part 3: Combine Both ---")
user_prompt = "Write a short poem about a robot learning to feel"
user_temp = 0.85
print(f"\nCustom Prompt: {user_prompt} | Temp: {user_temp}")
print(get_response(user_prompt, user_temp))