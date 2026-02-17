class EmbeddingService:
    embeddingProvider = None

    def __init__( self, embeddingProvider ):
        self.embeddingProvider = embeddingProvider

    def embed_chunks( self, chunks ):
        embeddings = self.embeddingProvider.embed_chunks( chunks )
        return embeddings
