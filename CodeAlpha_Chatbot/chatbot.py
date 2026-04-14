def get_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hello! How can I help you?"

    elif "bus pass" in user_input:
        return "You can book a bus pass from the dashboard."

    elif "price" in user_input:
        return "Prices depend on source and destination."

    elif "bye" in user_input:
        return "Goodbye! Have a nice day 😊"

    else:
        return "Sorry, I didn't understand that."