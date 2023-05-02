import argparse
import openai
import platform
import time


# function to generate chat completion
def chat(_messages, _max_tokens, _temp):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=_max_tokens,
        temperature=_temp,
        messages=_messages,
    )
    reply = response.choices[0].message.content
    tokens = response.usage.total_tokens
    return {"reply": reply, "tokens": tokens}


# set up argparse
parser = argparse.ArgumentParser(description="GPT console co-pilot")
parser.add_argument("query", type=str, help="enter your query")
parser.add_argument(
    "--tokens",
    type=int,
    default=50,
    help="the maximum number of tokens to generate in the completion",
)
parser.add_argument("--temp", type=float, default=0, help="between 0.0 and 2.0")
args = parser.parse_args()


# main function
def main():
    system_prompt = f"You are a professional bot that assists developers and systems administrators. This means you provide concise, helpful responses to the user's query, in one sentence when possible! Current environment: {platform.system()} {platform.release()}"
    color = "\033[36m"
    reset = "\033[0m"
    messages = []
    messages += [{"role": "system", "content": system_prompt}]
    messages += [{"role": "user", "content": args.query}]
    output = chat(messages, args.tokens, args.temp)
    print("[" + str(output["tokens"]) + f"] {color}", end="")
    for char in output["reply"]:
        print(char, end="", flush=True)
        time.sleep(0.005)
    print(f"{reset}")


# call main function
if __name__ == "__main__":
    main()
