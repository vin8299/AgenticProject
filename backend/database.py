import os
from functools import lru_cache

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# Order lookups are hot during a chat session; cache them to cut DB round trips.
@lru_cache(maxsize=512)
def get_order(order_id):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM orders WHERE order_id = %s",
        (order_id,)
    )

    order = cursor.fetchone()

    cursor.close()
    conn.close()

    return order


def save_message(session_id, role, message):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO support_messages
        (session_id, role, message)
        VALUES (%s, %s, %s,%s)
        """,
        (session_id, role, message)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_history(session_id):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT role, message
        FROM support_messages
        WHERE session_id LIKE %s
        ORDER BY created_at DESC
        LIMIT 10
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return list(reversed(rows))
