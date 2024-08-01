import os
import secrets

import dotenv
import streamlit as st

import actions

dotenv.load_dotenv('./.env')


# Assign a Session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = secrets.token_hex(8)
    

# ----- SIDE BAR -----
with st.sidebar:
    
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

    host = st.text_input(
        label = 'Server URL',
        key = 'HOST',
        placeholder = 'http://localhost:11434',
        value = os.getenv('OLLAMA_HOST')
    )
    
    model = st.text_input(
        label = 'Model',
        key = 'MODEL',
        placeholder = 'llama3',
        value = os.getenv('OLLAMA_MODEL')
    )
    
    temperature = st.slider(
        label = 'Temperature',
        key = 'TEMPERATURE',
        min_value = 0.5,
        max_value = 0.9,
        step = 0.01,
        value = 0.75
    )
 
    connect, clear = st.columns(2)
    
    with connect:
        _connect = st.button(
            label = 'Connect',
            key = 'connect',
            on_click = actions.check_server,
            use_container_width = True
        )
            
    with clear:
        _clear = st.button(
            label = 'Clear',
            key = 'clear',
            on_click = actions.clear_chat_history,
            use_container_width = True
        )

# ----- MAIN PAGE -----            

st.title('Chatbot')
st.markdown(f"You can start your Conversation with: `{st.session_state.get('MODEL')}`")
    
if st.session_state.get('langchain_messages'):
    for idx, message in enumerate(st.session_state.get('langchain_messages'), start=1):
        _user = 'human' if idx % 2 else 'assistant'
        with st.chat_message(_user):
            st.write(message.content)

user_input = st.chat_input(key = 'user_input', on_submit = actions.get_response)

if user_input:
    with st.chat_message('human'):
        st.write(user_input)
        
response = st.session_state.get('response')
if response:
    with st.chat_message('assistant'):
        st.write_stream(response)
    st.session_state['response'] = None
