#!/home/mishi/.config/bash/scripts/llmvenv

# import standard modules
import argparse
import importlib
import logging
import os
import platform
import sys
import time
# import custom modules
from colorama import Fore, Style

# configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# map model names to environment variables
# env variables should hold model names, e.g., `export CLAUDE_OPUS="claude-3-opus-20240229"`
model_env_mapping = {
    "gpt-3.5": "GPT_3_5",
    "gpt-4": "GPT_4",
    "claude-haiku": "CLAUDE_HAIKU",
    "claude-sonnet": "CLAUDE_SONNET",
    "claude-opus": "CLAUDE_OPUS"
}

# define the default system prompt. includes platform details to prime bot's reply
system_prompt = f"Concisely execute the grokked user instruction. Environment: {platform.system()} {platform.release()}"


# function to set script arguments with argparse
def set_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("--model", default="gpt-3.5", choices=model_env_mapping.keys())
    parser.add_argument("--temp", default=1.0, type=float)
    parser.add_argument("--tokens", default=100, type=int)
    parser.add_argument("--system-prompt", default=system_prompt)
    return parser.parse_args()


# function to load module from modules/[vendor]/completion.py
def get_module(model):
    # determine vendor based on model name
    vendor = "openai" if "gpt-" in model else "anthropic" if "claude-" in model else None
    # construct module path based on vendor
    sys.path.append('/home/mishi/.config/llm')
    _module_path = f"modules.{vendor}.completion"
    # import the appropriate module
    return importlib.import_module(_module_path)


# function to read model name from environment variable
def get_model(model):
    # get environment variable corresponding to the model
    model_env_var = model_env_mapping.get(model, "")
    # get the actual model name from the environment
    model_name = os.getenv(model_env_var)
    return model_name


def get_response(chat, user_prompt, model, temp, tokens, system_prompt):
     # generate chat completion from user input
    response = chat.generate(
        _system_prompt=system_prompt, 
        _user_prompt=user_prompt,
        _max_tokens=tokens,
        _temperature=temp,
        _model=model)
    # extract response content and token details
    reply = response["content"]
    prompt_tokens = response["prompt_tokens"]
    completion_tokens = response["completion_tokens"]
    total_tokens = response["total_tokens"]
    return reply, prompt_tokens, completion_tokens, total_tokens


def main():
    # setup script parameters and log details
    args = set_argparse()
    logging.info(f"Model {args.model} selected")
    logging.info(f"System prompt set to: {args.system_prompt}")
    logging.info(f"User prompt set to: {args.prompt}")

    # import appropriate completion module for vendor
    completion_module = get_module(args.model)

    # access chat completion class from imported module
    chat = completion_module.Completion()
    logging.info(f"Loading completion module {completion_module}")

    # determine actual model name
    model = get_model(args.model)
    logging.info(f"Using model {model}, temperature {args.temp}, max tokens {args.tokens}")
    
    # generate response using the chat completion
    reply, prompt_tokens, completion_tokens, total_tokens = get_response(chat, args.prompt, model, args.temp, args.tokens, args.system_prompt)
    logging.info(f"Tokens: {prompt_tokens} (prompt) + {completion_tokens} (completion) = {total_tokens} (total)")

    # print output to console with colored font in a scrolling typewriter effect
    print(f"🤖 {Fore.CYAN}", end="")
    for char in reply:
        print(char, end="", flush=True)
        time.sleep(0.005)
    print(f"{Style.RESET_ALL}")


# main entry point to script
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # log any errors during script execution
        logging.exception(e)
