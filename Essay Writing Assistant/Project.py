import os
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

from colorama import Fore,init,Style

init(autoreset=True)

client = genai.Client(api_key=GEMINI_API_KEY)



def generate_response(prompt, temperature=0.3):
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=config_params
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"
    

def get_essay_details():
    print(f"{Fore.CYAN} AI Writing Assistant ")

    topic = input(f"{Fore.MAGENTA} Enter the topic of your essay: ")

    essay_type = input(f"{Fore.MAGENTA} Enter the type of your essay: ")


    print(f"{Fore.CYAN} Select the desired word count: ")
    print(f"{Fore.YELLOW}1. 300 Words")
    print(f"{Fore.YELLOW}2. 900 Words")
    print(f"{Fore.YELLOW}3. 1200 Words")
    print(f"{Fore.YELLOW}4. 2000 Words")


    word_count_choice = int(input(f"{Fore.MAGENTA}Enter your choice: "))

    word_count_dict = {"1":"300","2":"900","3":"1200","4":"2000"}
    length = word_count_dict.get(word_count_choice,"300")

    target_audience = input(f"{Fore.MAGENTA} Enter the target audience of your essay: ")


    stance = input(f"{Fore.MAGENTA}What is your stance on the topic: {topic}")

    specific_points = input(f"{Fore.MAGENTA}Enter specific points you want to include in your essay: ")

    references = input(f"{Fore.MAGENTA}Enter references you want to include in your essay: ")

    writing_style = input(f"{Fore.MAGENTA}Enter the writing style: ")

    outline_needed = input(f"{Fore.MAGENTA}Would you like an outline for your essay? (yes/no): ")

    return {
        "topic":topic,
        "essay_type":essay_type,
        "length":length,
        "target_audience":target_audience,
        "stance":stance,
        "specific_points":specific_points,
        "references":references,
        "writing_style":writing_style,
        "outline_needed":outline_needed
    }


def generate_essay_content(details):
    temperature = float(input(f"{Fore.MAGENTA}Enter the temperature: "))
    introduction_prompt = f"Write an introduction for an {details["essay_type"]} essay about {details["topic"]} on the topic of {details["stance"]}"

    introduction = generate_response(introduction_prompt, temperature)
    print(f"{Fore.CYAN} Generating introduction...")

    print(f"{Fore.GREEN} + {introduction}")

    body_style = input(f"{Fore.MAGENTA}Enter the body style: ")
    body_prompt = f"Write a {body_style} body for an {details['essay_type']} essay about {details['topic']} on the topic of {details['stance']}"
    body =  generate_response(body_prompt, temperature)
    print(f"{Fore.CYAN} Generating body...")
    print(f"{Fore.GREEN} + {body}")

    conclusion_prompt = f"Write a conclusion for an {details['essay_type']} essay about {details['topic']} on the topic of {details['stance']}"
    conclusion = generate_response(conclusion_prompt, temperature)
    print(f"{Fore.CYAN} Generating conclusion...")
    print(f"{Fore.GREEN} + {conclusion}")



def feedback_and_refinement():
    satisfaction = input(f"{Fore.MAGENTA}How satisfied are you with the generated essay? (satisfied/unsatisfied): ")

    if satisfaction == "unsatisfied":
        feedback_prompt = input(f"{Fore.MAGENTA}Enter your feedback: ")
        generate_response(feedback_prompt)
        print(f"{Fore.CYAN} Generating feedback...")

    else:
        print(f"{Fore.CYAN} Essay generation completed.")




def run_activity():
    print(f"{Fore.CYAN} AI Writing Assistant")


    details = get_essay_details()

    generate_essay_content(details)

    feedback_and_refinement()


if __name__ == "__main__":
    run_activity()