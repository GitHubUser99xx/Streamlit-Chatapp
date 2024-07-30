import streamlit as st
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

class ChatBot:
    
    @property
    def chat_template(self):
        return ChatPromptTemplate.from_messages([
            ("system", "Your task is to answer the user's queries as accurately as possible"),
            ("placeholder", "{chat_history}"),
            ("user", "{input}")
        ])
        
    @property
    def llm(self):
        return ChatOllama(
            base_url=st.session_state.get("base_url"),
            model=st.session_state.get("model"),
            temperature=st.session_state.get("temperature"),
            timeout=600,
            keep_alive=3600
        )

    @property
    def chain(self):
        return RunnableWithMessageHistory(
            self.chat_template | self.llm | StrOutputParser(),
            lambda x: StreamlitChatMessageHistory("chat_history")
        )
        
    def invoke(self, message: str):
        return self.chain.invoke(
            {"input": message},
            {"configurable": {"session_id": st.session_state.get("session_id")}}
        )
        
    def stream(self, message: str):
        yield self.chain.stream(
            {"input": message},
            config={"configurable": {"session_id": st.session_state.get("session_id")}}
        )
        