import requests
import random
import html

EDUCATION_CATAGORY_ID = 8
API_URL = f"https://opentdb.com/api.php?amount=10&category={EDUCATION_CATAGORY_ID}&type=multiple"


def get_education_quetsions():
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        if data["response_code"] == 0:
            return data["results"]
    return None


def run_quiz():
    questions = get_education_quetsions()

    if not questions:
        print("Failed to fetch questions.")
        return
    

    score = 0

    print("Welcome to the Education Quiz! \n")

    for i, q in enumerate(questions,1):
        question = html.unescape(q["question"])
        correct = html.unescape(q["correct_answer"])
        incorrects = [html.unescape(a) for a in q["incorrect_answers"]]

        options = incorrects + [correct]

        random.shuffle(options)

        print(f"Question{i}: {question}")

        for idx, opt in enumerate(options, 1):
            print(f"{idx}: {opt}")


        
        while True:
            try:
                choice =  int(input("Enter your choice (1/2/3/4): "))

                if 1 <= choice <= 4:
                    break
            
            except ValueError:
                pass
        
        if options[choice - 1] == correct:
            print("Correct!")

            score += 1
        
        else:
            print(f"Incorrect. The correct answer is: {correct}")
    
    print(f"Your score: {score}/{len(questions)}")
    print(f"Percentage: {score / len(questions) * 100:.2f}%")


if __name__ == "__main__":
    run_quiz()