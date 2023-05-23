import argparse
import openai
import platform
import time

# base prompt
default_prompt = f"""

You are a professional bot that assists developers and systems administrators.
You reply only with one-line commands or brief concise responses, no commentary!
Current environment: {platform.system()} {platform.release()}

"""

# constants
default_model = "gpt-3.5-turbo"
default_tokens = 150
default_temp = 0
color = "\033[36m"
reset = "\033[0m"


# function to generate chat completion
def chat(messages, max_tokens, temp, model):
    response = openai.ChatCompletion.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temp,
        messages=messages,
    )
    reply = response.choices[0].message.content
    tokens = response.usage.total_tokens
    return {"reply": reply, "tokens": tokens}


# function to be called
def generate_response(
    query, tokens=default_tokens, temp=default_temp, model=default_model
):
    system_prompt = default_prompt
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]
    output = chat(messages, tokens, temp, model)
    return output


def main():
    # setup argparse
    parser = argparse.ArgumentParser(description="GPT console co-pilot")
    parser.add_argument("query", type=str, help="enter your query")
    parser.add_argument(
        "--tokens",
        type=int,
        default=default_tokens,
        help="the maximum number of tokens to generate in the completion",
    )
    parser.add_argument(
        "--temp", type=float, default=default_temp, help="between 0.0 and 2.0"
    )
    parser.add_argument("--model", type=str, default=default_model, help="")
    args = parser.parse_args()

    # generate completion
    output = generate_response(args.query, args.tokens, args.temp, args.model)

    # print formatted completion
    print("[" + str(output["tokens"]) + f"] {color}", end="")
    for char in output["reply"]:
        print(char, end="", flush=True)
        time.sleep(0.005)
    print(f"{reset}")


if __name__ == "__main__":
    main()
