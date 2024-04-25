#!/home/mishi/.config/bash/scripts/llmvenv-py
# uses: rofi dunst

# import modules
import os
import subprocess
import sys

# import custom modules
sys.path.append('/home/mishi/.config/llm')
from modules.openai import completion

# define the request parameters
MODEL = os.environ.get('GPT_3_5')
TEMPERATURE = 1
MAX_TOKENS = 200
SYSTEM_PROMPT = "Be concise and friendly."

# function to run rofi
def rofi_run():
    rofi_command = ['rofi', '-dmenu', '-p', '🤖', '-theme', 'rofibot']
    result = subprocess.run(rofi_command, capture_output=True, text=True).stdout.strip()
    return result

# main entry point to script
if __name__ == "__main__":
    # set the user prompt to the rofi input
    user_prompt = rofi_run()
    if not user_prompt:
        print("User canceled. Exiting.")
    else:
        # display user input
        print(f"{user_prompt}")

        # generate chat completion
        chat = completion.Completion()
        response = chat.generate(
            _system_prompt=SYSTEM_PROMPT,
            _user_prompt=user_prompt,
            _max_tokens=MAX_TOKENS,
            _temperature=TEMPERATURE,
            _model=MODEL)

        # display output
        reply = response["content"]
        print(f"> {reply}")

        # send notification
        dunstify_command = ['dunstify', 'Bot reply', reply, '-a', 'rofibot']
        subprocess.run(dunstify_command)
