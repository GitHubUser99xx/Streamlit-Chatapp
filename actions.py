import requests
import streamlit as st
from langchain_community.chat_message_histories import \
    StreamlitChatMessageHistory
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory


@st.cache_resource
def build_chain(url: str, model: str, temperature: float):
    if any(item is None for item in [url, model, temperature]):
        st.error('Invalid Ollama Parameters')
        
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "Your task is to answer the user's queries as accurately as possible."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])
    
    llm = ChatOllama(
        base_url = url,
        model = model,
        temperature = temperature,
        timeout = 600,
        keep_alive = 3600
    )
    
    memory_chain = RunnableWithMessageHistory(
        chat_template | llm | StrOutputParser(),
        lambda x: StreamlitChatMessageHistory('langchain_messages')
    )
    return memory_chain
    

def get_response():
    chain = build_chain(
        url = st.session_state.get('HOST'),
        model = st.session_state.get('MODEL'),
        temperature = st.session_state.get('TEMPERATURE')
    )
    response = chain.stream(
        {'input': st.session_state.get('user_input')},
        config = {'configurable': {'session_id': st.session_state.get('session_id')}}
    )
    st.session_state['response'] = response


def clear_chat_history():
    if st.session_state.get('clear'):
        st.session_state['langchain_messages'] = list()
        
        
def check_server():
    url = st.session_state.get('HOST')
    try:
        response = requests.head(url)
        assert response.status_code == 200
        
    except Exception as e:
        st.error("Unable to connect to Ollama Server")