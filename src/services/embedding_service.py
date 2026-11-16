class EmbeddingService:
    embeddingProvider = None

    def __init__( self, embeddingProvider ):
        self.embeddingProvider = embeddingProvider

    def embed_documents( self, documents ):
        embeddings = self.embeddingProvider.embed_documents( documents )
        return embeddings

    def embed_query( self, query ):
        vector = self.embeddingProvider.embed_query( query )
        return vector
