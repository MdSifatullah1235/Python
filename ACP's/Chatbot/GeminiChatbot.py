from google import genai
import config
from colorama import init, Style, Fore

init(autoreset=True)

client = genai.Client(api_key=config.GEMINI_API_KEY)

def run_chatbot():
    chat = client.chats.create(model="gemini-2.0-flash")

    print(f"{Fore.GREEN}Chatbot: {Style.RESET_ALL}Hello! How can I assist you today?")

    while True:
        try:
            user_msg = input(f'{Fore.YELLOW} You: {Style.RESET_ALL}')
            
            if user_msg.lower() in ["bye", "exit", "quit", "end", "stop"]:
                print(f"{Fore.GREEN} Have a nice day! {Style.RESET_ALL}")
                break

            response = chat.send_message(user_msg)
            print(f"{Fore.GREEN} Chatbot: {Style.RESET_ALL}{response.text}", flush=True)
        
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":    
    run_chatbot()