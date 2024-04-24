import anthropic

class Completion:
    def __init__(self):
        self.client = anthropic.Anthropic()

    # function to generate a chat completion
    def generate(self, _system_prompt, _user_prompt, _max_tokens, _temperature, _model):
        _messages = [
            {"role": "user", "content": _user_prompt}
        ]

        _response = self.client.messages.create(
            system = _system_prompt,
            max_tokens=_max_tokens,
            temperature=_temperature,
            model=_model,
            messages=_messages
        )

        _content = _response.content[0].text
        _input_tokens = _response.usage.input_tokens
        _output_tokens = _response.usage.output_tokens
        _total_tokens = _input_tokens + _output_tokens

        return {
            "content": _content,
            "prompt_tokens": _input_tokens,
            "completion_tokens": _output_tokens,
            "total_tokens": _total_tokens
        }
