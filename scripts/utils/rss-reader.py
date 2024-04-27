#!/home/mishi/.config/bash/scripts/llmvenv-py
# uses: feedparser rofi

# import standard modules
from datetime import datetime
import os
import subprocess
import sys

# import custom modules
import feedparser

# import completion module
sys.path.append('/home/mishi/.config/llm')
from modules.cohere import completion

# define which language model to use
MODEL = os.environ.get('COHERE_CMDR_PLUS')

# define how many entries to return from which feed
FEED_URL = "https://feeds.bbci.co.uk/news/world/rss.xml"
FEED_SIZE = 10

# define the request parameters
# don't set temperature too low or it will just repeat back entry titles
TEMPERATURE = 0.5
MAX_TOKENS = 300

SYSTEM_PROMPT = f"""This is an RSS news feed. Categorise and provide a concise summary of each item using the following formatting guidelines:
- Succinctly format each line in approximately ten (10) words
- Avoid simply repeating titles
- Ensure to include all key information, e.g., locations, main players, implications understood and highlighted
- Categorise each item concisely, e.g., "France", "RU/UA conflict", "Hurricane"
- Return {FEED_SIZE} lines, one for each item
- Format the output line for each as follows: `category_name > concise_summary`
Include no outside text or additional commentary."""

# function to parse the RSS feed and return a list of entries
def rss_reader(link, items_to_return):
    # parse RSS feed
    feed = feedparser.parse(link)

    # store returned entries in list
    items = []
    for index, feed_entry in enumerate(feed.entries[:(items_to_return)], start=1):
        item = f"Index:{index} Title:\"{feed_entry['title']}\", Content:\"{feed_entry['summary']}\""
        items.append(item)
    
    # error check
    if (len(items) != items_to_return):
        print(f"[CRIT] {link} did not return expected entries ({items_to_return})")
        sys.exit(1)

    return items

def main():
    # set the user prompt to a string containing the returned RSS entries
    USER_PROMPT = str(rss_reader(FEED_URL, FEED_SIZE))

    # generate the completion
    chat = completion.Completion()
    response = chat.generate(
        _system_prompt=SYSTEM_PROMPT,
        _user_prompt=USER_PROMPT,
        _max_tokens=MAX_TOKENS,
        _temperature=TEMPERATURE,
        _model=MODEL)

    # store output
    reply = response["content"]
    tokens = response["total_tokens"]

    # split reply string into individual lines for rofi
    replies = reply.split('\n')

    # escape special characters and remove any blank lines
    replies = [line.strip().replace("$", "\\$") for line in replies if line.strip()]

    # join the non-blank lines with newline characters
    replies_rofi = "\n".join(replies)

    # set title of notification/response
    title = f"Today's news for {tokens} tokens via {MODEL} | {datetime.today().date()}"

    # display output in console
    print(f"{title}:\n{replies_rofi}")

    # display output using rofi
    rofi_command = f'rofi -dmenu -mesg "{title}" <<< "{replies_rofi}" -theme "rss-reader" -theme-str "listview {{lines: {FEED_SIZE};}}"'
    subprocess.run(rofi_command, shell=True)

# main entry point to script
if __name__ == "__main__":
    main()