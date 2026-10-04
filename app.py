import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise SystemExit("Add your Claude API key as ANTHROPIC_API_KEY in .env.")

client = Anthropic(api_key=api_key)

MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

SYSTEM_PROMPT = """
You are Nova, the customer support assistant for NovaShop.

You help customers with:
- Product questions
- Orders
- Shipping
- Returns
- Refunds
- Damaged products
- Escalation

Rules:
1. Be concise and professional.
2. Never invent order information.
3. If order information is unavailable, ask for the order ID.
4. If the customer asks for a human, offer escalation.
5. Never invent company policies.
"""

while True:

    question = input("\nCustomer: ")

    if question.lower() in ["exit", "quit"]:
        break

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}]
    )

    print("\nNova:", "\n".join(
        block.text for block in response.content if block.type == "text"
    ))
