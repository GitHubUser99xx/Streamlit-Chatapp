import streamlit as st
from langchain_community.chat_message_histories import \
    StreamlitChatMessageHistory
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory

from logger import basic_logger


@st.cache_resource
def build_chain(url: str, model: str, temperature: float):
    # argument validation
    if any(item is None for item in [url, model, temperature]):
        basic_logger.critical("Ollama Parameters contain NoneType")
        return
    
    # Load the Chain
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "Your task is to answer the user's queries as accurately as possible."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])
    
    basic_logger.debug(f"Ollama Params: {dict(host=url, model=model, temperature=temperature)}")
    llm = ChatOllama(
        base_url=url,
        model=model,
        temperature=temperature,
        timeout=600,
        keep_alive=3600
    )
    
    memory_chain = RunnableWithMessageHistory(
        chat_template | llm | StrOutputParser(),
        lambda x: StreamlitChatMessageHistory("chat_history")
    )
    
    basic_logger.debug("Successfully loaded the chain to streamlit session_state")
    st.session_state["chain"] = memory_chain    
    return memory_chain
