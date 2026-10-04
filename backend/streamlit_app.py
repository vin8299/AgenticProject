import streamlit as st
import requests


API_URL = "http://localhost:8000/chat"


st.set_page_config(
    page_title="NovaShop Support",
    page_icon="🛍️"
)


st.title("🛍️ NovaShop AI Support")

st.caption(
    "Ask about products, shipping, returns or your order."
)


if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


prompt = st.chat_input(
    "How can Nova help you?"
)


if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.write(prompt)


    response = requests.post(
        API_URL,
        json={
            "session_id": "streamlit-user",
            "message": prompt
        }
    )


    answer = response.json()["reply"]


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    with st.chat_message("assistant"):

        st.write(answer)
