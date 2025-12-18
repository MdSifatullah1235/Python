import requests
import json
import os
import io
from colorama import init,Style,Fore
from PIL import Image

init(autoreset=True)

def query_hf_api_key(api_url,payload=None,headers=None,files=None,method="post"):
    try:
        if method.lower == "post":
            response = requests.post(api_url,data=payload,headers=headers,files=files)
        else:
            response = requests.get(api_url,data=payload,headers=headers,files=files)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code: {response.status_code}")
        return response.content
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        return None


def get_basic_caption(image,model="nlpconnect/vit-gpt2-image-captioning"):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    headers = {"Authorization": f"Bearer {api_url}"}
    response = requests.post(api_url, headers=headers, files={"image": buffered})
    result = response.json()
    if isinstance(result,dict) and "error" in result:
        raise Exception(result["error"])
    caption = result[0].get("generated_text","No caption generated.")
    return caption


def generate_text(prompt, model="gpt2",max_new_tokens = 60):
    print(f"{Fore.YELLOW}Enter the path of the image file:")
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs":prompt,"max_new_tokens":max_new_tokens}
    text_bytes = query_hf_api_key(api_url,payload=payload)
    try:
        result = json.laods(text_bytes.decode("utf-8"))
    except Exception as e:
        raise Exception("Failed to decode JSON response.")
    if isinstance(result,dict)  and     "error" in result:
        raise Exception(result["error"])
    generated = result[0].get("generated_text","No text generated.")
    return generated


def truncate_text(text,word_limit):
    words = text.strip().split()
    return " ".join(words[:word_limit])

def print_menu():
    print(f"{Fore.GREEN}Select an option:")
    print(f"{Fore.YELLOW}1.caption")
    print(f"{Fore.YELLOW}2.desc")
    print(f"{Fore.YELLOW}3.summary")
    print(f"{Fore.YELLOW}4.exit")
    choice = int(input("Enter your choice: "))
    return choice

def main():
    image_path = input("Enter the path of the image file: ")
    if not os.path.exists(image_path)
        print(f"{Fore.RED}Error: Image file not found.")
        return
    
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        return
    
    basic_caption = get_basic_caption(image)
    print(f"{Fore.GREEN}Basic caption: {basic_caption}")

    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            caption = generate_text(basic_caption)
            print(f"{Fore.GREEN}Caption: {caption}")
        
        elif choice == "2":
            prompt_text = input("Enter the prompt text: ")
            try:
                generated = generate_text(prompt_text)
                desc = truncate_text(generated,30)

            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
                return
            print(f"{Fore.GREEN}Description: {desc}")
        elif choice == "3":
            prompt_text = input("Enter the prompt text: ")
            try:
                generated = generate_text(prompt_text,max_new_tokens=60)
                summary = truncate_text(generated,30)
            
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
                return
            print(f"{Fore.GREEN}Summary: {summary}")
        elif choice == "4":
            print(f"{Fore.GREEN}Exiting...")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")


if __name__ == "__main__":
    main()