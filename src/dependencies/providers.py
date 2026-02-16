from pathlib import Path

from ..infrastructure import LocalFileStorage

def get_file_storage():
    uploads_dir = Path( "uploads" )
    uploads_dir.mkdir( parents=True, exist_ok=True )

    fileStorage = LocalFileStorage( base_dir = uploads_dir )

    return fileStorage
