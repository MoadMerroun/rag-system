from pathlib import Path
from uuid import uuid4

class LocalFileStorage:
    def __init__( self, base_dir: Path ):
        self.base_dir = base_dir

    def save( self, file_name: str, content: bytes ):
        suffix = Path( file_name ).suffix

        file_path = self.base_dir / f"{uuid4()}{suffix}"

        file_path.write_bytes( content )

        return str( file_path )
