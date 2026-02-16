from fastapi import Depends

from ..services import DocumentService
from .providers import get_file_storage

def get_document_service( fileStorage = Depends( get_file_storage ) ):
    document_service = DocumentService( fileStorage = fileStorage )

    return document_service
