#!/usr/bin/env python3

import openai
import os
import subprocess

THEME = "~/.config/rofi/themes/console-helper.rasi"
MODEL = os.environ.get("OPENAI_MODEL")


# function to generate chat completion
def chat(messages):
    response = openai.ChatCompletion.create(
        temperature=0,
        max_tokens=150,
        model=MODEL,
        messages=messages,
    )
    reply = response.choices[0].message.content
    return {"reply": reply}


# function to generate response
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
    rofi_cmd = [
        "rofi",
        "-dmenu",
        "-p",
        "🤖 ",
        "-theme",
        THEME,
    ]
    user_input = subprocess.check_output(rofi_cmd, universal_newlines=True).strip()
    chat = generate_response(user_input)
    chat_output = chat["reply"]

    # Display the output in rofi
    rofi_cmd = [
        "rofi",
        "-e",
        "🤖 " + chat_output,
        "-theme",
        THEME,
    ]
    subprocess.run(rofi_cmd)


if __name__ == "__main__":
    main()
