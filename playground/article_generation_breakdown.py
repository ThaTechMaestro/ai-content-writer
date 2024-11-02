from typing import List, Any, Dict
from langchain.chains import LLMChain
from langchain_community.vectorstores.chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage




'''
This class Handles memory
'''
class OnlyStoreAIMemory(ConversationBufferMemory):
    
    '''
    Stores only model response in memory
    '''
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        input_str, output_str = self._get_input_output(inputs, outputs)
        self.chat_memory.add_ai_message(output_str)


class ContentGenerator:
    def __init__(
        self,
        topic: str,
        outline: Any,
        questions_and_answers: dict,
        chunk_size: int=400,
        chunk_overlap: int=100,
        ):
        
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        
        self.topic = topic
        self.outline = outline 
        self.questions_and_answers = questions_and_answers
        
        prompt = f"""
        Act as a content SEO writer.
        You are currently writing a blog post on topic: {self.topic}.
        This is the outline of the blog post: {self.outline.json()}. You will be responsible for writing the blog post sections.
        ---
        Use your previous AI messages to avoid repeating yourself as you continually re-write the blog post sections.
        """
        
        chat = ChatOpenAI(model="gpt-3.5-turbo-16k")
        memory = OnlyStoreAIMemory(
            llm=chat,
            memory_key="chat_history",
            return_messages=True,
            max_token_limit=1200,
        )
        
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{human_input}"),
            ]
        )
        
        self.blog_post_chain = LLMChain(
            llm=chat, prompt=chat_prompt, memory=memory, output_key="blog_post"
        )
        self.chroma_db = None
        
        def split_and_vectorize_documents(self, text_documents):
            chunked_docs = self.text_splitter.split_docyments(text_documents)
            self.chroma_db = Chroma