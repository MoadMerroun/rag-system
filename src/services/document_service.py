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
        filename = file.filename or "upload.pdf"
        file_path = self.upload( file, filename )
        document = self.load( file_path )
        chunks = self.split( document )

        # A PDF with no extractable text (e.g. a scan) produces no chunks.
        if not chunks:
            return 0

        documents, metadatas, ids = self._prepare_chunks( chunks, filename )
        embeddings = self.embeddingService.embed_documents( documents )
        self.vectorStore.save( vectors = embeddings, documents = documents, metadatas = metadatas, ids = ids )

        return len( chunks )

    def _prepare_chunks( self, chunks, filename ):
        documents = []
        metadatas = []
        ids = []

        for i, chunk in enumerate( chunks ):
            documents.append( chunk.page_content )
            # Keep the original file name so answers can cite it as a source.
            metadatas.append( { **chunk.metadata, "filename": filename } )
            ids.append( f"{chunk.metadata.get('source')}-{chunk.metadata.get('page', 0)}-{i}" )

        return documents, metadatas, ids

    def upload( self, file, filename ):
        content = file.file.read()
        file_path = self.fileStorage.save( file_name = filename, content = content )

        return file_path

    def load( self, file_path ):
        return self.loader.load( file_path )

    def split( self, document ):
        return self.splitter.split( document )
