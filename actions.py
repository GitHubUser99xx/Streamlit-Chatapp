from typing import Iterator, Optional

import streamlit as st

from logger import basic_logger
from chatbot import build_chain

def user_submits_model_config():
    basic_logger.debug("Submit Button pressed. Adding Parameters to Session")
    build_chain(
        url=st.session_state.get("HOST"),
        model=st.session_state.get("MODEL"),
        temperature=st.session_state.get("TEMPERATURE")
    )


def user_clears_chat_history():
    basic_logger.debug("Deleting Chat History")
    st.session_state.pop("chat_history")
    

def ai_generates_response():
    # retrieve the conversation chain & user input
    chatbot = st.session_state.get("chain")
    user_input = st.session_state.get("user_input")
    
    # generate response
    return chatbot.stream(
        {"input": user_input},
        config={"configurable": {"session_id": st.session_state.get("session_id")}}
    )
    

def user_submits_message():
    # retrieve the chatbot
    response = ai_generates_response()
    
    # display the response
    with st.container():
        with st.chat_message("assistant"):
            st.write_stream(response)


def display_message(user: str, message: Optional[str] = None):
    """
    Displays a message either from the User or
    the Assistant.
    """
    # validate user parameter
    if user not in {"human", "assistant"}:
        raise ValueError(f"Invalid parameter: {user=}")
    
    # check if an empty message is sent
    if message is None:
        return
    
    # display the message
    with st.container():
        with st.chat_message(user):
            st.markdown(message)
    return


def display_chat_history():
    if "chat_history" in st.session_state:
        basic_logger.debug(f"({st.session_state.session_id}): Updating chat history")
        for idx, message in enumerate(st.session_state.get("chat_history"), start=1):
            user = "assistant" if idx % 2 == 0 else "human"
            display_message(user, message.content)
        return


def stream_message(response: Iterator):
    if response is None:
        return
    basic_logger.debug(f"({st.session_state.get("session_id")}): Displaying response from Assistant")
    with st.container():
        with st.chat_message("assistant"):
            st.write_stream(response)
