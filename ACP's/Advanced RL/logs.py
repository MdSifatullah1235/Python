from script import counter, improved_response

logs_list = {}
while True:
    logs_list[counter] = improved_response

    user_choice = input("Do you want to see the logs list: ")
    if user_choice.lower() == "yes":
        print(logs_list)
    else:
        print("Ok!")