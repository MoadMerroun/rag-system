from fastapi import APIRouter, Depends, UploadFile

from ..dependencies import get_document_service, get_rag_service

routers = APIRouter()

@routers.post( "/documents" )
async def upload( file: UploadFile, documentService = Depends( get_document_service ) ):
    embeddings = documentService.process( file )

    return embeddings

@routers.post( "/ask" )
async def ask( message: str, ragService = Depends( get_rag_service ) ):
    response = ragService.ask( message )

    return response
