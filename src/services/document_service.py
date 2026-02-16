class DocumentService:
    fileStorage = None

    def __init__( self, fileStorage ):
        self.fileStorage = fileStorage

    def process( self, file ):
        file_path = self.upload( file )
        return file_path

    def upload( self, file ):
        content = file.file.read()
        file_path = self.fileStorage.save( file_name = file.filename or "upload.pdf", content = content )

        return file_path
