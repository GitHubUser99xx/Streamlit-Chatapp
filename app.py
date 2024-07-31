import secrets

import streamlit as st

from logger import basic_logger
import actions


# Assign a Session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = secrets.token_hex(16)
    basic_logger.debug(f"Starting a new Session. Session-ID: {st.session_state.get("session_id")}")

# Sidebar
with st.sidebar:
    # Sidebar::header
    with st.container():
        st.title("Ollama Chat")
        st.markdown(
            """
            [Ollama](https://github.com/ollama/ollama) is a runtime & API server that helps users to
            run LLMs in the [GGUF](https://huggingface.co/docs/hub/gguf) format using
            [llama.cpp](https://github.com/ggerganov/llama.cpp).
            
            The list of all supported models offered by Ollama can be found at the
            [Model Library](https://ollama.com/library)
            """
        )

    # Sidebar::ollama-parameters
    with st.container():
        host = st.text_input(
            "Server URL",
            key="HOST",
            placeholder="http://localhost:11434"
        )
        
        model = st.text_input(
            "LLM",
            key="MODEL",
            placeholder="llama3"
        )
        
        temperature = st.slider(
            "Temperature",
            key="TEMPERATURE",
            min_value=0.5,
            max_value=0.9,
            step=0.01,
            value=0.75
        )
 
    # Sidebar::buttons
    with st.container():
        submit, clear = st.columns(2)
        with submit:
            st.button(
                label="Submit",
                key="submit",
                on_click=actions.user_submits_model_config,
                use_container_width=True
            )
                
        with clear:
            st.button(
                label="Clear",
                key="clear",
                on_click=actions.user_clears_chat_history,
                use_container_width=True
            )
            

# Main Page
# ---------
# This page will show the chat messages between
# the User and Assistant.

# Display the Title & Subheader
st.title("Chatbot")
st.markdown(f"You can start your Conversation with: `{st.session_state.get("MODEL")}`")
    
# Display the chat history
display_chat_history()

# User Input 
st.chat_input(key="user_input", on_submit=actions.user_submits_message)
display_message("human", st.session_state.get("user_input"))