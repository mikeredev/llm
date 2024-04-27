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
FEED_SIZE = 2

# define the request parameters
# don't set temperature too low or it will just repeat back entry titles
TEMPERATURE = 0.5
MAX_TOKENS = 300
SYSTEM_PROMPT = f"""This is an RSS news feed. Concisely refactor each of these entries, using one (1) representative emoji for each 'category' (e.g., national flag).
Ensure to include all key information, e.g., locations, key players, implications understood and highlighted.
Avoid repeating titles or using colons.
Succinctly format each line in approx ten (10) words like this:
``` example
⚔️ Fighting continues in Greenland as the invading US forces push north.
🇫🇷 The French town of Rouen plays host to the Japanese football team.
🐧 Zoo officials in Tromso, Norway, hunt sixteen escaped penguins.
[etc]
```
Include no outside text or additional commentary."""

# function to parse the RSS feed and return a list of entries
def rss_reader():
    # parse RSS feed
    feed = feedparser.parse(FEED_URL)

    # store returned entries in list
    items = []
    for index, feed_entry in enumerate(feed.entries[:(FEED_SIZE)], start=1):
        item = f"Entry {index}: ({feed_entry['title']}): Summary ({feed_entry['summary']})"
        items.append(item)
    
    # error check
    if (len(items) != FEED_SIZE):
        print(f"[CRIT] {FEED_URL} did not return expected entries ({FEED_SIZE})")
        sys.exit(1)

    return items

# main entry point to script
if __name__ == "__main__":
    # set the user prompt to a string containing the returned RSS entries
    USER_PROMPT = str(rss_reader())

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
    title = f"{datetime.today().date()} > Today's news for {tokens} tokens"
    # display output in console
    print(f"{title}:\n{replies_rofi}")

    # display output using rofi
    rofi_command = f'rofi -dmenu -mesg "{title}" <<< "{replies_rofi}" -theme rss-reader -theme-str "listview {{lines: {FEED_SIZE};}}"'
    subprocess.run(rofi_command, shell=True)