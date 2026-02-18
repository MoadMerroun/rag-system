from fastapi import Depends

from ..services import DocumentService
from .providers import get_file_storage, get_loader, get_splitter, get_embedding, get_vector_store

def get_document_service(
    fileStorage = Depends( get_file_storage ),
    loader = Depends( get_loader ),
    splitter = Depends( get_splitter ),
    embeddingService = Depends( get_embedding ),
    vectorStore = Depends( get_vector_store )
):
    document_service = DocumentService(
        fileStorage = fileStorage,
        loader = loader,
        splitter = splitter,
        embeddingService = embeddingService,
        vectorStore = vectorStore
    )

    return document_service
