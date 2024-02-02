#### OpenAI chatbots

| script                   | description                                     | screenshot |
|:-------------------------|:------------------------------------------------|:-----------|
| gpt-chatbot-console      | console-based AI helper                         |[link](https://github-production-user-asset-6210df.s3.amazonaws.com/132297919/265040102-b23cbcfb-a62f-45b8-8ab5-606e350dd692.png)|
| gpt-chatbot-conversation | realistic context-aware conversations           |[link](https://github-production-user-asset-6210df.s3.amazonaws.com/132297919/265040873-babf680f-7cfb-4234-a9fe-92882aded02b.png)
| gpt-chatbot-gui-ctkinter | friendly customtkinter chatbot GUI              |[link](https://github-production-user-asset-6210df.s3.amazonaws.com/132297919/265036944-327720d1-67fb-403c-85de-f2c38da110ee.png)| 
| gpt-chatbot-pinecone     | chatbot with memory recollection using pinecone |[link](https://github.com/mikeredev/openai/assets/132297919/e38ed6ca-68c7-4d05-be3b-ff88e57c8903)|
| rofi-gpt                 | ask simple queries via a rofi interface         |[link](https://github.com/mikeredev/openai/assets/132297919/2576e76b-cc8a-408a-9f5b-3213f68746d2)|
| gpt-news                 | parses and summarises an RSS feed               |[link](https://github.com/mikeredev/openai/assets/132297919/e57d5172-c82a-4e54-be73-8319e8dbae80)|

### Quick Notes
gpt-chatbot-console - create chat completions from console. useful for sysadmin tasks/quick queries.

gpt-chatbot-conversation - appends previous chats to the history for contextual awareness.

gpt-chatbot-gui-ctkinter - an SMS-like chat interface

gpt-chatbot-pinecone - summarises conversations into "memories" and adds to a vector database (similar to: [2308.15022](https://arxiv.org/abs/2308.15022))

gpt-chatbot-rofi  - similar to gpt-chatbot-console but runs in the rofi menu

gpt-news - can be used to summarise any RSS feed, although the prompt is designed for parsing BBC News (e.g., removing author names, publication titles, etc., from final output)
