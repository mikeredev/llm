# import modules
from openai import OpenAI

# function to generate a chat completion using the OpenAI API
def chat_completion(_system_prompt, _user_prompt, _max_tokens, _temperature, _model):

    client = OpenAI()
    _messages = [
        {"role": "system", "content": _system_prompt},
        {"role": "user", "content": _user_prompt},
    ]

    _response = client.chat.completions.create(
        max_tokens=_max_tokens,
        temperature=_temperature,
        model=_model,
        messages=_messages
    )

    _content = _response.choices[0].message.content
    _completion_tokens = _response.usage.completion_tokens
    _prompt_tokens = _response.usage.prompt_tokens
    _total_tokens = _response.usage.total_tokens

    return {
        "content": _content,
        "completion_tokens": _completion_tokens,
        "prompt_tokens": _prompt_tokens,
        "total_tokens": _total_tokens
    }
