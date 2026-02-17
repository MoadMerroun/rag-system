from fastapi import APIRouter, Depends, UploadFile

from ..dependencies import get_document_service

routers = APIRouter()

@routers.post( "/documents" )
async def upload( file: UploadFile, documentService = Depends( get_document_service ) ):
    embeddings = documentService.process( file )

    return embeddings
