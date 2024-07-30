import streamlit as st
import secrets
from chatbot import ChatBot

def display_message(user: str, message: str):
    assert user in {"human", "assistant"}
    if message is None:
        return
    with st.container():
        with st.chat_message(user):
            st.markdown(message)
    return


def stream_message(response):
    if response == "":
        return 
    with st.container():
        with st.chat_message("assistant"):
            st.write_stream(response)


def display_chat_history():
    if "chat_history" in st.session_state:
        for idx, message in enumerate(st.session_state.get("chat_history"), start=1):
            user = "assistant" if idx % 2 == 0 else "human"
            display_message(user, message.content)
        return

# Assign a Session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = secrets.token_hex(16)
    st.session_state["initialized"] = False
    
# initialize the Chatbot
bot = ChatBot()
    
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
        HOST = st.text_input("Server URL", "http://localhost:11434")
        MODEL = st.text_input("LLM", "llama3")
        TEMPERATURE = st.slider("Temperature", min_value=0.5, max_value=0.9, value=0.75, step=0.01)
        
    # Sidebar::buttons
    with st.container():
        submit, reset = st.columns(2)
        with submit:
            if st.button("Submit", use_container_width=True):
                st.session_state["base_url"] = HOST
                st.session_state["model"] = MODEL
                st.session_state["temperature"] = TEMPERATURE
                st.session_state["initialized"] = True
                
        with reset:
            if st.button("Reset", use_container_width=True) and st.session_state["initialized"]:
                st.session_state["base_url"] = ""
                st.session_state["model"] = ""
                st.session_state["temperature"] = 0.7
                st.session_state["initialized"] = False
                st.session_state.pop("chat_history")
    
# Main Page
st.title("Chatbot")
if not st.session_state["initialized"]:
    st.markdown("Please input the Ollama Configuration from the sidebar")
else:
    st.markdown(f"__Model Selected__: {st.session_state["model"]}")

# Display the chat history
display_chat_history()

# User Message
user_message = st.chat_input()
display_message("human", user_message)

# # Generated Message
response = bot.stream(user_message) if user_message else ""
stream_message(response)