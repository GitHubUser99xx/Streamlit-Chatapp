import logging
import logging.config

import streamlit as st
import yaml
from langchain_community.chat_message_histories import \
    StreamlitChatMessageHistory
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import (RunnableSequence,
                                      RunnableWithMessageHistory)

with open("log-config.yaml", "r") as f:
    logging.config.dictConfig(yaml.load(f, yaml.SafeLoader))
    basic_logger = logging.getLogger("basic")
    basic_logger.setLevel(logging.DEBUG)


@st.cache_resource
def build_chain(url: str, model: str, temperature: float):
    # argument validation
    if any(item is None for item in [url, model, temperature]):
        basic_logger.critical("Ollama Parameters contain NoneType")
        return
    
    basic_logger.debug("Loading ChatPromptTemplate")
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "Your task is to answer the user's queries as accurately as possible."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])
    
    basic_logger.debug("Loading ChatOllama")
    basic_logger.debug(f"Using params: {dict(host=url, model=model, temperature=temperature)}")
    llm = ChatOllama(
        base_url=url,
        model=model,
        temperature=temperature,
        timeout=600,
        keep_alive=3600
    )
    
    basic_logger.debug("Loading RunnableSequence")
    conversation_chain = RunnableSequence(
        chat_template,
        llm,
        StrOutputParser(),
        name="Chain-Conversation"
    )
    
    basic_logger.debug("Loading RunnableWithMessageHistory")
    memory_chain = RunnableWithMessageHistory(
        conversation_chain,
        lambda x: StreamlitChatMessageHistory("chat_history")
    )
    
    return memory_chain
