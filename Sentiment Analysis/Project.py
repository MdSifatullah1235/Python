from textblob import TextBlob
from colorama import Fore,init,Style


init(autoreset=True)
user_name = input(f"{Fore.MAGENTA}Enter your name: ")
print(f"{Fore.CYAN} Hi There! {user_name}{Style.RESET_ALL} How can I help you today?")
print(f"{Fore.CYAN} {Style.RESET_ALL}How are you today?")
mood_input = input(f"{Fore.YELLOW}{Style.RESET_ALL}You: ")

analysis = TextBlob(mood_input)
polarity = analysis.sentiment.polarity
subjectivity = analysis.sentiment.subjectivity


if polarity > 0.1:
    print(f"{Fore.GREEN} You are happy today! {Style.RESET_ALL}")

elif polarity < -0.1:
    print(f"{Fore.RED} You are sad today! {Style.RESET_ALL}")

else:
    print(f"{Fore.YELLOW} You are neutral today! {Style.RESET_ALL}")