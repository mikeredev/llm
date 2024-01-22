""" gpt-chatbot-rofi.py
desc:       creates a chat completion using the OpenAI API
requires:   openai
usage:      python ~/data/scripts/system-mgmt/gpt-chatbot-rofi.py
i3:         bindsym $mod+x exec --no-startup-id sh -c 'python ~/data/scripts/system-mgmt/gpt-chatbot-rofi.py'
"""

# import modules
import os
import subprocess

# import non-standard/custom modules
import openai_chat

# main
if __name__ == "__main__":
    try:
        # Open rofi bar and get user input
        rofi_cmd = ["rofi", "-dmenu", "-p", "🤖 ", "-theme", "dmenu"]
        user_input = subprocess.check_output(rofi_cmd, universal_newlines=True).strip()

        # send the user_input to the chatcompletion function
        response = openai_chat.response(
            "Reply helpfully in one concise line.",
            user_input
            # within the confines of the specified environment, endeavour to understand the user's query, then provide a comprehensive, succinct reply
        )

        # Display the output in rofi
        rofi_cmd = ["rofi", "-e", "🤖 " + response["output"], "-theme", "dmenu"]
        subprocess.run(rofi_cmd)

    except Exception as e:
        subprocess.run(
            f"notify-send 'rofi-gpt-chatbot' 'error: {e}'",
            shell=True,
        )
