"""RAG Pipeline Module

This module handles the document loading, processing, and RAG pipeline creation.
Uses the latest LangChain API for compatibility and stability.
"""

import os
import warnings
# Suppress pydantic v1 compatibility warning on Python 3.14+
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality", category=UserWarning)
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()


class RAGPipeline:
    """Handles document loading, embedding, and RAG pipeline creation."""
    
    def __init__(self, openai_api_key: str = None):
        """
        Initialize the RAG pipeline.
        
        Args:
            openai_api_key: OpenAI API key. If None, will use OPENAI_API_KEY from environment.
        """
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables or arguments")
        
        self.documents = []
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.embeddings = OpenAIEmbeddings(api_key=self.api_key)
        
    def load_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Load a PDF file and extract documents.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of loaded documents
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        self.documents.extend(documents)
        
        return documents
    
    def load_text_file(self, txt_path: str) -> List[Dict[str, Any]]:
        """
        Load a text file and split it into documents.
        
        Args:
            txt_path: Path to the text file
            
        Returns:
            List of loaded documents
        """
        if not os.path.exists(txt_path):
            raise FileNotFoundError(f"Text file not found: {txt_path}")
        
        try:
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(txt_path)
            documents = loader.load()
            self.documents.extend(documents)
            return documents
        except Exception as e:
            raise Exception(f"Error loading text file: {str(e)}")
    
    def split_documents(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict[str, Any]]:
        """
        Split documents into smaller chunks for better processing.
        
        Args:
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of split documents
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        split_docs = splitter.split_documents(self.documents)
        self.documents = split_docs
        
        return split_docs
    
    def create_vector_store(self) -> FAISS:
        """
        Create a FAISS vector store from documents.
        
        Returns:
            FAISS vector store
        """
        if not self.documents:
            raise ValueError("No documents loaded. Please load documents first.")
        
        self.vector_store = FAISS.from_documents(
            documents=self.documents,
            embedding=self.embeddings
        )
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        return self.vector_store
    
    def setup_chain(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7) -> Any:
        """
        Setup the RAG chain with the vector store and LLM using LCEL.
        
        Args:
            model_name: OpenAI model to use
            temperature: Temperature setting for the model
            
        Returns:
            The configured RAG chain
        """
        if not self.retriever:
            raise ValueError("Vector store not created. Please create vector store first.")
        
        llm = ChatOpenAI(
            api_key=self.api_key,
            model=model_name,
            temperature=temperature
        )
        
        system_prompt = """You are a helpful assistant that answers questions based on provided documents. 
Use the context provided to answer the user's question accurately. 
If the answer is not found in the context, say "I don't have enough information to answer this question."

Context:
{context}"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        def format_docs(docs):
            """Format retrieved documents for context."""
            return "\n\n".join(doc.page_content for doc in docs)
        
        # Build LCEL chain
        self.chain = (
            {
                "context": self.retriever | format_docs,
                "input": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return self.chain
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG pipeline with a question.
        
        Args:
            question: The question to ask
            
        Returns:
            Dictionary with 'answer' and 'context' keys
        """
        if not self.chain:
            raise ValueError("Chain not setup. Please setup the chain first.")
        
        # Get context documents
        context_docs = self.retriever.invoke(question)
        
        # Invoke the chain with the question
        answer = self.chain.invoke(question)
        
        return {
            "answer": answer,
            "context": context_docs
        }
    
    def save_vector_store(self, path: str) -> None:
        """
        Save the vector store to disk for later use.
        
        Args:
            path: Path to save the vector store
        """
        if not self.vector_store:
            raise ValueError("Vector store not created.")
        
        self.vector_store.save_local(path)
    
    def load_vector_store(self, path: str) -> FAISS:
        """
        Load a previously saved vector store.
        
        Args:
            path: Path to the saved vector store
            
        Returns:
            FAISS vector store
        """
        self.vector_store = FAISS.load_local(
            path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        return self.vector_store
