import cohere
import os

class Completion():
    def __init__(self):
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

    def generate(self, _system_prompt, _user_prompt, _max_tokens, _temperature, _model):
        response = self.co.chat(
            preamble=_system_prompt,
            message=_user_prompt,
            max_tokens=_max_tokens,
            temperature=_temperature,
            model=_model
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
