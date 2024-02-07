from openai import OpenAI

class Conversation():
    def __init__(self):
        self.client = OpenAI()
        self._messages = []

    # function to generate a chat completion
    def generate(self, _system_prompt, _user_prompt, _max_tokens, _temperature, _model):
        _response = self.client.chat.completions.create(
            max_tokens=_max_tokens,
            temperature=_temperature,
            model=_model,
            messages=self._messages
        )

        _content = _response.choices[0].message.content
        _prompt_tokens = _response.usage.prompt_tokens
        _completion_tokens = _response.usage.completion_tokens
        _total_tokens = _response.usage.total_tokens

        return {
            "content": _content,
            "prompt_tokens": _prompt_tokens,
            "completion_tokens": _completion_tokens,
            "total_tokens": _total_tokens
        }

    # function to get user input
    def get_user_input(self):
        user_prompt = input(f"[{self.token_counter}] > ")
        return user_prompt

    # function to update payload with latest message
    def update_payload(self, role, text):
        message = {"role":role, "content":text}
        self._messages.append(message)

    # function to update token count
    def update_token_count(self, tokens):
        self.token_counter += tokens
        self.message_counter += 1

    # function to prune earliest User and Assistant entries (system prompt is at index 0)
    def prune_history(self, size):
        if len(self._messages) > size:
            self._messages.pop(1)
            self._messages.pop(1)
