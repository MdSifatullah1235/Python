while True:
    user_input = input("Enter your task: ")
    to_do_list = []
    print(to_do_list)
    if user_input == "quit":
        break
    elif user_input == "remove":
        remove_input = int(input("Enter the item number you wnat to remove:"))
        to_do_list.pop(remove_input)
    else:
        to_do_list.append(user_input)
