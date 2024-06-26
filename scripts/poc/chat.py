#!/home/mishi/.config/llm/venv/bin/python
# uses: openai 1.10.0, colorama 0.4.6

# import modules
import sys
sys.path.append('/home/mishi/.config/llm')
from modules.openai import conversation
from colorama import Fore, Style
import time

# vars
SYSTEM_PROMPT="Reply in 15 words maximum."
MAX_HISTORY = 5

# instantiate objects
chat=conversation.Conversation()

# set system prompt
chat.update_payload("system", SYSTEM_PROMPT)
print(f"System prompt: {SYSTEM_PROMPT}")
chat.token_counter = 0
chat.message_counter = 0

# enter "chat" loop
while True:
    # get user input
    user_prompt = chat.get_user_input()

    # update payload with user input
    chat.update_payload("user", user_prompt)

    # generate completion
    response = chat.generate(
        _system_prompt=SYSTEM_PROMPT, 
        _user_prompt=user_prompt,
        _max_tokens=50,
        _temperature=1,
        _model="gpt-3.5-turbo")
    reply = response["content"]
    tokens = response["total_tokens"]

    # print output to console
    print(f"🤖 {Fore.CYAN}", end="")
    for char in reply:
        print(char, end="", flush=True)
        time.sleep(0.005)
    print(f"{Style.RESET_ALL}")

    # update payload with reply
    chat.update_payload("assistant", reply)

    # update token counter
    chat.update_token_count(tokens)

    # prune chat history
    chat.prune_history(MAX_HISTORY)
