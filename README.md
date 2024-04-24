### Setup
```bash
cd /path/to/this/repo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Contents
| script | description |
| :-     | :-          |
| ```modules/anthropic/completion.py``` | generate a single completion via claude |
| ```modules/openai/completion.py```    | generate a single completion via gpt |
| ```modules/openai/conversation.py```  | contextually-aware conversation, history pruning |
| ```scripts/bots/claude.py```          | generate a single completion via claude |
| ```scripts/bots/gpt.pt```             | generate a single completion via gpt |
| ```scripts/poc/chat.py```             | contextually-aware conversation, history pruning |
| ```scripts/poc/customtkinter.py```    | SMS-like chatbot GUI |  |
| ```scripts/poc/infinite-craft.py```   | explore chain-of-thought reasoning in [infinite craft](https://neal.fun/infinite-craft) game |
| ```scripts/poc/pinecone.py```         | summarize conversations, utilize memory recall |
| ```scripts/prompts/chaos-gpt.py```    | instantiate a character explore built-in biases |
| ```scripts/utils/rofi.py```           | generate a single completion via rofi |
| ```scripts/utils/rss-reader.py```     | parse and summarise an RSS feed |
