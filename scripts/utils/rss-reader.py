#!/home/mishi/.config/bash/scripts/llmvenv-py
# uses: feedparser rofi

# import standard modules
import argparse
from datetime import datetime
import logging
import os
import subprocess
import sys

# import custom modules
import feedparser

# import and configure llm completion
model = os.environ.get('COHERE_CMDR_PLUS')
sys.path.append('/home/mishi/.config/llm')
from modules.cohere import completion

# set model parameters
temperature = 0.5
max_tokens = 300

# default feed url and items to parse (override with script args)
feed_url = "https://feeds.bbci.co.uk/news/world/rss.xml"
feed_items = 2

# set system prompt
system_prompt = f"""This is an RSS news feed. Categorise and provide a concise summary of each item using these formatting guidelines:
- Succinctly format each line in approximately ten (10) words
- Avoid simply repeating titles
- Ensure to include all key information, e.g., locations, main players, implications understood and highlighted
- Categorise each item concisely, e.g., "France", "RU/UA conflict", "Hurricane"
- Return each Index entry on its own newline
- Format each individual output line as follows: `category_name > concise_summary`
Include no outside text or additional commentary."""


# function to setup argparse
def set_argparse():
    # supports defining feed url and total returned items
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=feed_url, \
        help = f"the RSS feed to read (defaults {feed_url})")
    parser.add_argument("--items", type=int, default=feed_items, \
        help = f"how many items to return from each feed (default: {feed_items})")
    parser.add_argument("--log-level", default="info", choices=["debug", "info", "warning", "error", "critical"], \
        help = "set log level (default: info)")
    return parser.parse_args()


# function to fetch RSS items
def get_rss_items(url, items):
    # use feedparser to fetch the RSS feed
    feed = feedparser.parse(url)
    logging.info(f"Fetching {items} items from {url}")

    # format each line and add to list
    rss_items = [
        f"Index:{index} Title:\"{entry['title']}\", Content:\"{entry['summary']}\""
        for index, entry in enumerate(feed.entries[:items], start=1)
    ]
    logging.info(rss_items)

    # check returned list is not empty
    if (len(rss_items) == 0):
        logging.error(f"No RSS feed items found at URL: {url}")
        sys.exit(1)

    # return a string of formatted RSS items
    return str(rss_items)


# function to generate chat completion
def get_response(_user_prompt, _system_prompt=system_prompt, **kwargs):
    # load the chat completion class
    chat = completion.Completion()

    # generate completion
    response = chat.generate(
        _system_prompt,
        _user_prompt,
        _model=model,
        _temperature=temperature,
        _max_tokens=max_tokens
    )

    # store output
    reply = response["content"]
    tokens = response["total_tokens"]
    logging.info(f"Generated reply for {tokens} tokens")
    return reply, tokens


# function to display output in rofi
def show_output(rss, total_tokens, items):
    # split reply into individual lines
    display_items = rss.split('\n')

    # escape special characters and remove any blank lines
    display_items = [line.strip().replace("$", "\\$") for line in display_items if line.strip()]

    # join the non-blank lines with newline characters
    display_list = "\n".join(display_items)

    # set display_title of notification/response
    display_title = f"Today's news for {total_tokens} tokens via {model} | {datetime.today().date()}"

    # display output in console
    print(f"{display_title}:\n{display_list}")

    # display output using rofi
    rofi_command = f'rofi -dmenu -mesg "{display_title}" <<< "{display_list}" -theme "rss-reader" -theme-str "listview {{lines: {items};}}"'
    subprocess.Popen(rofi_command, shell=True)
    logging.info("Results displayed")


# main function
def main():
    # setup logging and argparse
    args = set_argparse()
    logging.basicConfig(level=logging.getLevelName(args.log_level.upper()), format='%(levelname)s - %(message)s')

    # set url/items as default unless arguments are passed
    url = args.url
    items = args.items
    logging.info(f"Specified feed URL: {url}, specified items: {items}")

    # fetch RSS feed items
    rss_feed = get_rss_items(url, items)

    # pass formatted string of RSS items to language model for refactoring
    reply, total_tokens = get_response(rss_feed)

    # display output with rofi
    show_output(reply, total_tokens, items=items)


# main entry point to script
if __name__ == "__main__":
    main()
