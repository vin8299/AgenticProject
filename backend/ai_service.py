import os
import re

from dotenv import load_dotenv
from anthropic import Anthropic

from backend.database import (
    get_order,
    get_history,
    save_message
)

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise SystemExit("Add your Claude API key as ANTHROPIC_API_KEY in .env.")

client = Anthropic(api_key=api_key)

MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


SYSTEM_PROMPT = """
You are Nova, the AI customer-support assistant for NovaShop.

You help customers with:

- Product questions
- Order status
- Shipping
- Returns
- Refunds
- Damaged products
- Human escalation

Policies:

Returns:
Products can generally be returned within 30 days.

Damaged products:
Customers should contact support with their order ID.

Refunds:
Approved refunds normally return to the original payment method.

Important rules:

- Never invent order information.
- Use database context when available.
- If an order cannot be found, say so.
- Ask for an order ID when necessary.
- If the customer requests a human, recommend escalation.
"""


def find_order_id(message):

    match = re.match(
        r"ORD-\d{3,6}",
        message.upper()
    )

    return match.group(0) if match else None


def build_context(message):

    context = ""

    order_id = find_order_id(message)

    if order_id:

        order = get_order(order_id)

        if order:

            context += f"""
ORDER INFORMATION

Order ID: {order['order_id']}
Customer: {order['customer_name']}
Product: {order['product']}
Status: {order['status']}
Expected delivery: {order['expected_delivery']}
Total: ${order['total']}
"""

        else:

            context += f"""
Order {order_id} was not found.
"""

    return context


def ask_ai(session_id, message):

    save_message(
        session_id,
        "user",
        message
    )

    context = build_context(message)

    history = get_history(session_id)

    history_text = "\n".join(
        f"{item['role']}: {item['message']}"
        for item in history
    )

    prompt = f"""
Conversation history:

{history_text}

Business context:

{context}

Customer message:

{message}
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = "\n".join(
        block.text for block in response.content 
    )

    save_message(
        session_id,
        "assistant",
        answer
    )

    return answer

def stream_ai(message):

    context = build_context(message)

    prompt = f"""
Business context:

{context}

Customer:

{message}
"""

    with client.messages.stream(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user"}]
    ) as stream:
        yield from stream.text_stream
