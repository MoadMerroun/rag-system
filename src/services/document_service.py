class DocumentService:
    fileStorage = None
    loader = None
    splitter = None
    embeddingService = None

    def __init__( self, fileStorage, loader, splitter, embeddingService ):
        self.fileStorage = fileStorage
        self.loader = loader
        self.splitter = splitter
        self.embeddingService = embeddingService

    def process( self, file ):
        file_path = self.upload( file )
        document = self.load( file_path )
        chunks = self.split( document )
        documents = [ document.page_content for document in chunks ]
        embeddings = self.embeddingService.embed_documents( documents )

        return embeddings

    def upload( self, file ):
        content = file.file.read()
        file_path = self.fileStorage.save( file_name = file.filename or "upload.pdf", content = content )

        return file_path

    def load( self, file_path ):
        return self.loader.load( file_path )

    def split( self, document ):
        return self.splitter.split( document )
