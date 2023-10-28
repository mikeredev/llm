#!/usr/bin/env python3
""" gpt-news.py
desc:       provides a handy summary of the latest news updates (or any other RSS feed)
usage:      python ~/data/scripts/system-mgmt/gpt-news.py
"""

try:
    import openai_chat
    import subprocess
    from datetime import datetime
    import os
    import sys
    sys.path.append(
        f"/home/{os.getlogin()}/data/scripts/openai/venv/lib/python3.11/site-packages")
    import feedparser
    print("🤖")
except Exception as e:
    print(f"Failed to load custom modules: {e}")

rss_url = "https://feeds.bbci.co.uk/news/world/rss.xml"
feed = feedparser.parse(rss_url)

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d")

news = []
for i, entry in enumerate(feed.entries[:5], start=1):
    title = entry['title']
    summary = entry['summary']
    latest_news = f"{i} {title}: {summary}"
    news.append(latest_news)

reply = openai_chat.response(
    f"""
    It is {formatted_datetime}. K3 updates only. Read the below news headlines, synthesize the key information and class it as follows:
    K0: extraneous information, e.g., publication or author names
    K1: low-impact news items, e.g., celebrities or minor speculation
    K2: medium-impact news items, e.g., routine political developments
    K3: high-impact news items, e.g., accidents, deaths, major political developments
    Then give me a brief news update about only K3 news updates. Do not tell me about K0 or K1, and mention K2 only if deemed consequential.
    After synthesizing and categorizing the news items, give me a brief update in bullet-points, tailored for a busy individual in need of the key updates only.
    Do not reference the K classifiers in your reply!
    Keep your reply under 400 tokens, or three/four sentences.
    Review your response multiple times to ensure readability, clarity, and brevity.
    Format your reply like this:
        In today's important news:
        - important item 1
        - important item 2
        - (other important items)
    Say nothing else.
    """, str(news), tokens=400, temperature=0.2)
news_updates = reply["output"]
tokens = reply["total_tokens"]
subprocess.run(["dunstify", "-u", "critical", "-a", "pynews",
               f"{formatted_datetime} {tokens}", news_updates])
