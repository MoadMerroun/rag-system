class VectorStore:
    vectorStoreProvider = None

    def __init__( self, vectorStoreProvider ):
        self.vectorStoreProvider = vectorStoreProvider

    def save( self, vectors, documents, metadatas, ids ):
        res = self.vectorStoreProvider.save(
            vectors = vectors,
            documents = documents,
            metadatas = metadatas,
            ids = ids
        )

        return res
