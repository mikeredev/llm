""" gpt-chatbot-conversation.py
desc:       creates realistic conversation by passing previous replies back to the bot as context
requires:   openai, colorama
usage:      python gpt-chatbot-conversation.py
notes:      control token usage/cost by adjusting MAX_HISTORY. this represents the number of old replies to use as context.
"""

# import modules
import openai
from colorama import Fore, Style

# set constants
MODEL = "gpt-3.5-turbo"  # language model to be used
MAX_TOKENS = 100  # max output tokens
TEMPERATURE = 1.5  # set temperature
MAX_HISTORY = 7  # use odd number. max messages to pass to the chatbot for context
SYS_PROMPT = "Chat with the user."  # your default system instructions


def run(func, message, *args, **kwargs):
    print(f"{Style.RESET_ALL}=> {message}... ", end="")
    try:
        result = func(*args, **kwargs)
        str_result = f"{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}OK{Style.RESET_ALL} {Style.DIM}{str(result)}{Style.RESET_ALL}"
        print(str_result)
        return result
    except Exception as e:
        str_result = f"{Style.RESET_ALL}{Fore.LIGHTRED_EX}FAIL{Style.RESET_ALL}\n{Style.DIM}==> {str(e)}\n==> Stack trace follows{Style.RESET_ALL}"
        print(str_result)
        return result


class Conversation:
    def __init__(self):
        self.messages = [{"role": "system", "content": SYS_PROMPT}]
        self.counter_tokens = 0
        self.message_counter = 0

    # function to update payload with user input
    def update_payload(self, role, text):
        self.messages.append({"role": role, "content": text})
        return self.messages

    # function to update token count
    def update_token_count(self, tokens):
        self.counter_tokens += tokens
        self.message_counter += 1
        return f"{self.message_counter}@{self.counter_tokens}"

    # function to prune earliest User and Assistant entries
    def rotate_chatlog(self, MAX_HISTORY, len_messages):
        if len_messages >= MAX_HISTORY:
            self.messages.pop(1)
            self.messages.pop(1)
        return f"{len_messages}/{MAX_HISTORY}"

    # function to get user input
    def get_user_input(self):
        user_prompt = input(f"{Fore.LIGHTCYAN_EX}")
        return user_prompt

    # function to generate chat completion
    def get_bot_reply(self, messages):
        response = openai.ChatCompletion.create(
            model=MODEL, max_tokens=MAX_TOKENS, temperature=TEMPERATURE, messages=messages
        )
        reply = response.choices[0].message.content
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        print(f"{Fore.LIGHTCYAN_EX}\n==> {reply}{Style.RESET_ALL}")
        return {"reply": reply, "total_tokens": total_tokens, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens}

    def run(self):
        while True:
            # get the user input
            user_input = run(self.get_user_input, "send a message")

            # update payload with user input
            run(self.update_payload,
                "updating payload [user]", "user", user_input)

            # return chat completion
            bot_reply = run(
                self.get_bot_reply, "rendering LLM response", self.messages)

            # update payload with bot reply
            run(self.update_payload,
                "updating payload [bot]", "assistant", bot_reply["reply"])

            # update message and token counters
            counter_tokens = run(
                self.update_token_count, "updating token counter", bot_reply["total_tokens"])

            # prune oldest messages if needed
            run(self.rotate_chatlog,
                "updating history", MAX_HISTORY, len(self.messages))


# Enter main loop
if __name__ == "__main__":
    chat = Conversation()
    chat.run()
