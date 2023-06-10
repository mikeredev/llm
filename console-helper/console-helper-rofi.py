#!/usr/bin/env python3

import subprocess
import openai


# function to generate chat completion
def chat(messages):
    response = openai.ChatCompletion.create(
        temperature=0,
        max_tokens=150,
        model="gpt-3.5-turbo",
        messages=messages,
    )
    reply = response.choices[0].message.content
    tokens = response.usage.total_tokens
    return {"reply": reply, "tokens": tokens}


# function to be called
def generate_response(query):
    system_prompt = "Reply briefly and concisely all in one line."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]
    output = chat(messages)
    return output


def main():
    # Open rofi bar and get user input
    rofi_cmd = ["rofi", "-dmenu", "-p", "🤖 "]
    user_input = subprocess.check_output(rofi_cmd, universal_newlines=True).strip()
    chat = generate_response(user_input)
    chat_output = chat["reply"]

    # Display the output in rofi
    rofi_cmd = ["rofi", "-e", "🤖 " + chat_output]
    subprocess.run(rofi_cmd)

    # Show notif with output
    # subprocess.run(["notify-send", "gpt", chat_output])ai


if __name__ == "__main__":
    main()
