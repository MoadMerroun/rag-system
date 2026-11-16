from ..models import Chunk

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

    def similarity_search( self, vector, k = 4 ):
        result = self.vectorStoreProvider.similarity_search( [ vector ], k = k )

        # Chroma returns one list per query vector; we sent a single vector.
        texts = result[ "documents" ][ 0 ]
        metadatas = result[ "metadatas" ][ 0 ]

        return [ Chunk( text = text, metadata = metadata or {} ) for text, metadata in zip( texts, metadatas ) ]
