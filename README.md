# NovaShop support assistant

A command-line customer support assistant powered by Claude.

## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set these values in `.env` (this file is ignored by Git):

```dotenv
ANTHROPIC_API_KEY=your_claude_api_key_here
ANTHROPIC_MODEL=claude-sonnet-4-6
```

Run `python app.py`, then type your question. Type `exit` or `quit` to stop.

The app uses Anthropic's [Messages API](https://platform.claude.com/docs/en/api/python/messages/create).
Each question is sent independently with the NovaShop system prompt.
