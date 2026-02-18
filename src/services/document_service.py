class DocumentService:
    fileStorage = None
    loader = None
    splitter = None
    embeddingService = None
    vectorStore = None

    def __init__( self, fileStorage, loader, splitter, embeddingService, vectorStore ):
        self.fileStorage = fileStorage
        self.loader = loader
        self.splitter = splitter
        self.embeddingService = embeddingService
        self.vectorStore = vectorStore

    def process( self, file ):
        file_path = self.upload( file )
        document = self.load( file_path )
        chunks = self.split( document )
        documents, metadatas, ids = self._prepare_chunks( chunks )
        embeddings = self.embeddingService.embed_documents( documents )
        self.vectorStore.save( vectors = embeddings, documents = documents, metadatas = metadatas, ids = ids )

        return embeddings

    def _prepare_chunks( self, chunks ):
        documents = []
        metadatas = []
        ids = []

        for i, chunk in enumerate( chunks ):
            documents.append( chunk.page_content )
            metadatas.append( chunk.metadata )
            ids.append( f"{chunk.metadata.get('source')}-{chunk.metadata.get('page', 0)}-{i}" )

        return documents, metadatas, ids

    def upload( self, file ):
        content = file.file.read()
        file_path = self.fileStorage.save( file_name = file.filename or "upload.pdf", content = content )

        return file_path

    def load( self, file_path ):
        return self.loader.load( file_path )

    def split( self, document ):
        return self.splitter.split( document )
