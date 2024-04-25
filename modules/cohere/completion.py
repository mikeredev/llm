import cohere
import os

class Completion():
    def __init__(self):
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

    def generate(self, _system_prompt=None, _user_prompt=None, _max_tokens=None, _temperature=None, _model=None):
        response = self.co.chat(
            message=_user_prompt,
            model=_model,
            max_tokens=_max_tokens,
            temperature=_temperature,
            preamble=_system_prompt
        )

        content = response.text
        input_tokens = response.meta.tokens.input_tokens
        output_tokens = response.meta.tokens.output_tokens
        total_tokens = input_tokens + output_tokens

        return {
            "content": content,
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": total_tokens
        }
