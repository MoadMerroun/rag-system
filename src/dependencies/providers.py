from pathlib import Path

from ..infrastructure import LocalFileStorage, LangChainLoader, LangChainSplitter, OpenAIEmbedding, ChromaVectorStore, OpenAILlm
from ..prompts import RAG_PROMPT_TEMPLATE

def get_file_storage():
    uploads_dir = Path( "uploads" )
    uploads_dir.mkdir( parents=True, exist_ok=True )

    fileStorage = LocalFileStorage( base_dir = uploads_dir )

    return fileStorage

def get_loader():
    langChainLoader = LangChainLoader()
    return langChainLoader

def get_splitter():
    langChainSplitter = LangChainSplitter(
        chunk_size = 800,
        chunk_overlap = 80,
        length_function = len,
        is_separator_regex = False
    )

    return langChainSplitter

def get_embedding():
    openaiembedding = OpenAIEmbedding()
    return openaiembedding

def get_vector_store():
    chromaVectorStore = ChromaVectorStore()
    return chromaVectorStore

def get_llm_provider():
    llmProvider = OpenAILlm()
    return llmProvider

def get_prompt_template():
   return RAG_PROMPT_TEMPLATE
