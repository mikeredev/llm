#!/home/mishi/.config/llm/venv/bin/python
# uses: openai 1.10.0, colorama 0.4.6
# https://neal.fun/infinite-craft/

# import modules
import sys
import re
sys.path.append('/home/mishi/.config/llm')
from modules.openai import conversation
from colorama import Fore, Style
import time

# game vars
elements = ['water', 'fire', 'wind', 'earth']
goal = "Skyrim"
turns = 50

# vars
SYSTEM_PROMPT=f"""This is a crafting-game that requires long-term planning.
Pick two items that you haven't mixed recently. Your goal is to ultimately create '{goal}'.
Ensure your selection isn't in the recent history. The same recipes will always produce the same result. You can mix the same item with itself, e.g. tree + tree = forest. Consider which elements you need to reach your goal, e.g., a city might need buildings and people.
Format your reply like this:
I will craft item ID (name) and ID (name), e.g., 'I will now craft item 0 (fire) and 1 (wind), because [give a brief reaction to the last result, and explain in 10 words maximum your long-term chain-of-reasoning regarding the basic components needed to create the goal].'
"""

# instantiate objects
chat=conversation.Conversation()
recent=[]
result_history=[]
# set system prompt
chat.update_payload("system", SYSTEM_PROMPT)
print(f"System prompt: {SYSTEM_PROMPT}")
chat.token_counter = 0
chat.message_counter = 0

def split_reply(sentence):
    # Extract item IDs and element names enclosed in parentheses from the response
    items = re.findall(r'(\d+) \((.*?)\)', sentence)
    combined_names = ' + '.join([f"{item[0]} ({item[1]})" for item in items])
    return combined_names

def update_list(user_prompt):
    if user_prompt not in elements:
        elements.append(user_prompt)
        print(f"{Fore.GREEN}Added '{user_prompt}' to the list of known elements{Style.RESET_ALL}")
        recent[-1] = f"{recent[-1]}={user_prompt}"
        user_prompt = f"success! {user_prompt}"
    else:
        print(f"{Fore.YELLOW}Element '{user_prompt}' is already known{Style.RESET_ALL}")
        recent[-1] = f"{recent[-1]}={user_prompt}(FAIL)"
        user_prompt = f"fail ({user_prompt})"
        #recent.append(user_prompt)
    return user_prompt

def begin_game():
    user_prompt = "start here"
    return user_prompt

def end_game():
    print(elements)
    sys.exit(0)

def send_feedback(msg):
    if msg.startswith("!f"):
        return msg[3:].strip()


while True:
    # get user input
    user_prompt = chat.get_user_input()

    if "!s" in user_prompt:
        user_prompt = begin_game()
    elif "!q" in user_prompt:
        user_prompt = end_game()
    elif "!f" in user_prompt:
        feedback = send_feedback(user_prompt)
        user_prompt = f"FAIL. feedback from ADMIN: {feedback}"
    else:
        user_prompt = update_list(user_prompt)

    formatted_elements = ""
    for index, element in enumerate(elements):
        formatted_elements += f"{index} {element}, "
    # Remove the trailing comma and space
    known_elements = formatted_elements.rstrip(", ")


    # update payload with user input
    formatted_string = f"""```results (turn {chat.message_counter}/{turns})\n{user_prompt}\n```\n```last_5_turns\n{recent}\n```\n```known_elements\n{known_elements}\n```\nreminder, your goal is to create a '{goal}' element. review the recent turn history, and make a new selection!"""
    chat.update_payload("user", f"{formatted_string}")
    #print(formatted_string)

    # generate completion
    response = chat.generate(
        _system_prompt=SYSTEM_PROMPT, 
        _user_prompt=user_prompt,
        _max_tokens=50,
        _temperature=0.7,
        _model="gpt-3.5-turbo")
    reply = response["content"]
    tokens = response["total_tokens"]

    # print output to console
    print(f"{Fore.CYAN}", end="")
    for char in reply:
        print(char, end="", flush=True)
        time.sleep(0.005)
    print(f"{Style.RESET_ALL}")

    # update payload with reply
    chat.update_payload("assistant", reply)
    formatted_response = split_reply(reply)
    recent.append(formatted_response)

    # update token counter
    chat.update_token_count(tokens)

    # prune chat history
    chat.prune_history(3)

    if len(recent) > 5:
        recent.pop(0)
    
    print(f"{known_elements}")
