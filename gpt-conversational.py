import openai
import run_function
from colorama import Fore, Style

# set constants
MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 100
TEMPERATURE = 1.3

class Conversation:
    # initialise env
    def __init__(self):
        self.system_prompt = "Chat with the user."
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.counter_tokens = 0
        self.max_history = 7


    # function to get user input
    def get_user_input(self):
        user_prompt = input(f"{Fore.BLUE}")
        return user_prompt


    # function to update history with user input
    def update_payload(self, role, text):
        self.messages.append({"role": role, "content": text})
        return self.messages

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


    # function to update token count
    def update_token_count(self, tokens):
        self.counter_tokens += tokens
        return self.counter_tokens


    # function to prune history
    def prune_history(self, max_history, len_messages):
        if len_messages >= max_history:
            self.messages.pop(1)
            self.messages.pop(1)
        return f"{len_messages}/{self.max_history}"


    def run(self):
        while True:
            user_input = run_function.run(self.get_user_input, "type your query")
            run_function.run(self.update_payload, "updating payload [user]", "user", user_input)
            bot_reply = run_function.run(self.get_bot_reply, "rendering LLM response", self.messages)
            run_function.run(self.update_payload, "updating payload [bot]", "assistant", bot_reply["reply"])
            counter_tokens = run_function.run(self.update_token_count, "updating token counter", bot_reply["total_tokens"])
            run_function.run(self.prune_history, "pruning history", self.max_history, len(self.messages))


# enter main loop
new_chat = Conversation()
new_chat.run()
