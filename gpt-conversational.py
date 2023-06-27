import openai
import run_function
import subprocess
from colorama import Fore, Style


# function to get user input
def get_user_input(output="console"):
    user_prompt = input(f"{Fore.BLUE}")
    return user_prompt


# function to update history with user input
def update_history(role, text):
    if role == "system":
        messages.append({"role": "system", "content": text})
    elif role == "user":
        messages.append({"role": "user", "content": text})
    elif role == "assistant":
        messages.append({"role": "assistant", "content": text})
    return messages


# function to generate chat completion
def get_bot_reply(messages, output="console"):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", max_tokens=100, temperature=1.3, messages=messages
    )
    reply = response.choices[0].message.content
    tokens = response.usage.total_tokens
    if output == "notify":
        notify_cmd = ["notify-send", "gpt fren", reply, "-t", "10000"]
        subprocess.run(notify_cmd)
    print(f"{Fore.LIGHTCYAN_EX}\n==> {reply}{Style.RESET_ALL}")
    return {"reply": reply, "tokens": tokens}


# function to update token count
def update_token_count(counter_tokens, tokens):
    counter_tokens += tokens
    return counter_tokens


# function to update message history count
def update_message_count(counter_history, message_count):
    counter_history = message_count
    return counter_history


# function to prune history
def prune_history(max_history, len_messages):
    if len_messages >= max_history:
        messages.pop(1)
        messages.pop(1)
        return len_messages
    return "not needed"


# initialise env
system_prompt = "Chat with the user."
messages = [{"role": "system", "content": system_prompt}]
counter_tokens = 0
counter_history = 0
max_history = 7

# enter main loop
while True:
    user_input = run_function.run(get_user_input, "waiting on user input")
    run_function.run(
        update_history, "updating history with user input", "user", user_input
    )
    bot_reply = run_function.run(
        get_bot_reply, "rendering LLM response", messages, "notify"
    )
    run_function.run(
        update_history,
        "updating history with bot reply",
        "assistant",
        bot_reply["reply"],
    )
    counter_tokens = run_function.run(
        update_token_count,
        "updating token counter",
        counter_tokens,
        bot_reply["tokens"],
    )
    counter_history = run_function.run(
        update_message_count, "updating message count", counter_history, len(messages)
    )

    run_function.run(prune_history, "pruning history", max_history, len(messages))
