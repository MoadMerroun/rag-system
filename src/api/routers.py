from fastapi import APIRouter, Depends, UploadFile

from ..dependencies import get_document_service, get_rag_service
from ..schemas import UploadResponse, AskRequest, AskResponse, Source

routers = APIRouter()

# Plain `def` (not `async def`): the services make blocking calls (PDF parsing,
# OpenAI, Chroma), so FastAPI runs these handlers in a thread pool.

@routers.post( "/documents", response_model = UploadResponse )
def upload( file: UploadFile, documentService = Depends( get_document_service ) ):
    chunks = documentService.process( file )

    return UploadResponse( filename = file.filename or "upload.pdf", chunks = chunks )

@routers.post( "/ask", response_model = AskResponse )
def ask( request: AskRequest, ragService = Depends( get_rag_service ) ):
    answer, chunks = ragService.ask( request.question )

    sources = [
        Source( filename = chunk.metadata.get( "filename", "unknown" ), page = chunk.metadata.get( "page" ) )
        for chunk in chunks
    ]

    return AskResponse( answer = answer, sources = sources )
