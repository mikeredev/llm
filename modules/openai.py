from openai import OpenAI

class Completion:
    def __init__(self):
        self.client = OpenAI()

    def generate(self, _system_prompt, _user_prompt, _max_tokens, _temperature, _model):
        _messages = [
            {"role": "system", "content": _system_prompt},
            {"role": "user", "content": _user_prompt},
        ]

        _response = self.client.chat.completions.create(
            max_tokens=_max_tokens,
            temperature=_temperature,
            model=_model,
            messages=_messages
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
