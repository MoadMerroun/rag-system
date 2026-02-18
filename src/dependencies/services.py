from fastapi import Depends

from ..services import DocumentService, RagService, EmbeddingService, VectorStore, LlmService
from .providers import get_file_storage, get_loader, get_splitter, get_embedding, get_vector_store, get_llm_provider, get_prompt_template

def get_embedding_service( embeddingProvider = Depends( get_embedding ) ):
    embedding_service = EmbeddingService( embeddingProvider = embeddingProvider )

    return embedding_service

def get_vector_store_service( vectorStoreProvider = Depends( get_vector_store ) ):
    vector_store = VectorStore( vectorStoreProvider = vectorStoreProvider )

    return vector_store

def get_llm_service( llmProvider = Depends( get_llm_provider ), promptTemplate = Depends( get_prompt_template ) ):
    llm_service = LlmService( llmProvider = llmProvider, promptTemplate = promptTemplate )

    return llm_service

def get_document_service(
    fileStorage = Depends( get_file_storage ),
    loader = Depends( get_loader ),
    splitter = Depends( get_splitter ),
    embeddingService = Depends( get_embedding_service ),
    vectorStore = Depends( get_vector_store_service )
):
    document_service = DocumentService(
        fileStorage = fileStorage,
        loader = loader,
        splitter = splitter,
        embeddingService = embeddingService,
        vectorStore = vectorStore
    )

    return document_service

def get_rag_service(
    llmService = Depends( get_llm_service ),
    embeddingService = Depends( get_embedding_service ),
    vectorStore = Depends( get_vector_store_service )
):
    rag_service = RagService(
        llmService = llmService,
        embeddingService = embeddingService,
        vectorStore = vectorStore
    )

    return rag_service
