#!/bin/python
""" gpt-chatbot-console.py
desc:       console-based OpenAI chatbot
requires:   openai_chat, colorama
usage:      python gpt-chatbot-console.py "How do I..."
"""

# import modules
import argparse
import platform
import random
import time

# import non-standard/custom modules
from colorama import Fore, Style
import openai_chat

if __name__ == "__main__":
    # setup argparse and assign default values
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str)
    parser.add_argument("--tokens", type=int, default=openai_chat.tokens)
    parser.add_argument("--model", type=str, default=openai_chat.model)
    parser.add_argument("--temperature", type=float, default=openai_chat.temperature)
    args = parser.parse_args()

    # generate chat completion
    response = openai_chat.response(
        f"Reply briefly as an expert in {platform.system()} {platform.release()}",
        args.prompt,
        tokens=args.tokens,
        model=args.model,
        temperature=args.temperature,
    )

    # print formatted completion
    print(f"🤖 {Fore.CYAN}", end="")
    for char in response["output"]:
        print(char, end="", flush=True)
        time.sleep(0.005)
    print(f"{Style.RESET_ALL}")
