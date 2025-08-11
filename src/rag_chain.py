from langchain_groq import ChatGroq
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from src.config import Config

class RAGChain:
    def __init__(self, vstore):
        self.vstore = vstore
        self.llm = ChatGroq(model=Config.RAG_MODEL, temperature=0.5)
        self.history_store = {}

    def _get_history(self, session_id)->BaseChatMessageHistory:
        if session_id not in self.history_store:
            self.history_store[session_id]=ChatMessageHistory()
        return self.history_store[session_id]
    
    def build_chain(self):
        retriever = self.vstore.as_retriever(search_kwargs={"k":5})

        cxt_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the chat history and user question, rewrite it as a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an e-commerce assistant that answers product-related questions based on reviews and titles. Stay strictly within the given context. Be concise, helpful, and present answers in clear bullet points. Highlight product names for readability.
                CONTEXT: {context}
                QUESTION: {input}"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}") 
        ])

        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, cxt_prompt
        )

        qa_chain = create_stuff_documents_chain(
            self.llm, qa_prompt
        )

        rag_chain = create_retrieval_chain(
            history_aware_retriever, qa_chain
        )

        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )