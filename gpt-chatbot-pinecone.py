from datetime import datetime
import json
import openai
import os
import pinecone
from uuid import uuid4

# define pinecone constants
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_REGION = "asia-northeast1-gcp"
PINECONE_INDEX = "test1"
# define openai constants
MODEL_EMBED = "text-embedding-ada-002"
MODEL_CHAT = "gpt-3.5-turbo"
TEMPERATURE = 0
MAX_TOKENS = 50
# define prompts
INST_STANDARD = (
    "Chat with your old friend. Review memories and history to inform your replies"
)
INST_SUMMARY = "Record general information you learned about the user. Continue building a profile on them. Be concise. Only record facts, no commentary! Write in first person in one sentence, e.g., 'I learned that...'"
# define other constants
MIN_DISTANCE = 0.8
CONV_LENGTH = 2
USERID = "ADMIN"
AIID = "BOT"
DEBUG_HDR = "\033[34m"
DEBUG_TXT = "\033[36m"
DATA = "\033[2m"
SUCCESS = "\033[32m ✓"
FAIL = "\033[31m ✗"
RESET = "\033[0m"
PRINT_DEBUG = True


# function to print debug information
def print_debug(title, text):
    if PRINT_DEBUG:
        print(f"{DEBUG_HDR}[{title.upper()}]{DEBUG_TXT} " + str(text) + f"{RESET}")


# function to initialise pinecone
def pinecone_connect(_api_key, _region):
    pinecone.init(api_key=_api_key, environment=_region)


# function to create embeddings
def embed(_embed_input):
    response = openai.Embedding.create(model=MODEL_EMBED, input=_embed_input)
    vector = response["data"][0]["embedding"]
    return vector


# function to generate chat completion
def chat_completion(
    _user_input, _system_prompt, _bootstrap_prompt=None, _max_tokens=MAX_TOKENS
):
    response = openai.ChatCompletion.create(
        model=MODEL_CHAT,
        max_tokens=_max_tokens,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": str(_bootstrap_prompt) + "\n" + str(_system_prompt),
            },
            {"role": "user", "content": _user_input},
        ],
    )
    reply = response.choices[0].message.content
    tokens = response.usage.total_tokens
    print_debug(
        "chat",
        f"user prompt: {DATA}{_user_input}{RESET}{DEBUG_TXT}, system prompt: {DATA}{_system_prompt}{RESET}{DEBUG_TXT}, bootstrap prompt: {DATA}{_bootstrap_prompt}{RESET}",
    )
    return {"reply": reply, "tokens": tokens}


# initialise environment
pinecone_connect(PINECONE_API_KEY, PINECONE_REGION)
VDB = pinecone.Index(PINECONE_INDEX)
history = []
history_metadata_str = ""
message_counter = 0
tokens_total = 0
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

# enter main loop
while True:
    # get user input and vectorize it
    user_input = input(f"{USERID}: ")
    print_debug("embd", "vectorizing user input...")
    vector = embed(user_input)

    # search for vector matches before responding
    print_debug("vctr", "searching vector DB...")
    results = VDB.query(vector, top_k=1, include_metadata=True)

    system_input = ""
    # load top result returned
    if results["matches"]:
        match = results["matches"][0]
        print_debug(
            f"vctr",
            f"top match => distance: {DATA}{round(match['score'],4)}{RESET}{DEBUG_TXT}, data: {DATA}{match['metadata']}",
        )

        # check if distance is above min threshold
        if float(match["score"]) >= MIN_DISTANCE:
            # load top match as memory if above threshold
            print_debug(
                "vctr",
                f"threshold {MIN_DISTANCE} met, loading match... {SUCCESS}",
            )
            system_input = f"you recalled a memory! `{match['metadata']}` "
        else:
            # or ignore it if not
            print_debug(
                "vctr",
                f"threshold {MIN_DISTANCE} not met, ignoring match... {FAIL}",
            )

    # or just respond normally if no results returned
    else:
        print_debug("vctr", "no results returned")

    # get bot reply
    if history_metadata_str:
        system_input += f"conversation log! `{history_metadata_str}`"
    print_debug("chat", "generating response...")
    chat_output = chat_completion(
        _user_input=user_input,
        _system_prompt=system_input,
        _bootstrap_prompt=INST_STANDARD,
    )

    # update in-memory conversation history
    message_counter += 1
    history_metadata = {
        "message": message_counter,
        "timestamp": timestamp,
        USERID + " (user)": user_input,
        AIID + " (you)": chat_output["reply"],
    }
    history.append({"metadata": history_metadata})
    # cut off any older conversations
    if len(history) > CONV_LENGTH:
        history.pop(0)
    # prepare history metadata
    history_metadata_str = ", ".join([str(entry["metadata"]) for entry in history])
    print_debug("chat", "cycle " + str(message_counter) + "/" + str(CONV_LENGTH))

    # update total token cost counter
    tokens_total += chat_output["tokens"]

    # summarise the key points of the conversation if we've reached max length
    if message_counter == CONV_LENGTH:
        print_debug("chat", "summarizing chat history...")
        summary = chat_completion(
            _user_input=history_metadata_str,
            _system_prompt=INST_SUMMARY,
            _max_tokens=MAX_TOKENS * 2,
        )
        message_counter = 0
        tokens_total += summary["tokens"]
        print_debug("chat", f"memory created: {DATA}" + summary["reply"])

        # create payload
        print_debug("vctr", "creating payload...")
        vector = embed(summary["reply"])
        unique_id = str(uuid4())
        payload = [
            (unique_id, vector, {"memory": summary["reply"], "timestamp": timestamp})
        ]

        # upsert payload
        print_debug("vctr", "upserting payload...")
        VDB.upsert(payload)

    # render chat_output
    cost_per_token = 0.000002
    estd_cost = tokens_total * cost_per_token
    print_debug(
        "chat",
        "rendering reply for "
        + str(chat_output["tokens"])
        + " tokens, total "
        + str(tokens_total)
        + " (approx. "
        + str(round(estd_cost, 4))
        + " USD)",
    )
    print(f"{AIID}: " + chat_output["reply"])
