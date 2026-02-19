import chromadb

class ChromaVectorStore:
    chromaVectorStore = None
    collection_name = None

    def __init__( self, collection_name = "documents" ):
        self.chromaVectorStore = chromadb.Client()
        self.collection_name = collection_name
        self.chromaVectorStore.get_or_create_collection( name = self.collection_name )

    def save( self, vectors, documents, metadatas, ids ):
        collection = self.chromaVectorStore.get_collection( name = self.collection_name )

        collection.add(
            ids = ids,
            embeddings = vectors,
            documents = documents,
            metadatas = metadatas,
        )

    def similarity_search( self, vectors ):
        collection = self.chromaVectorStore.get_collection( name = self.collection_name )

        return collection.query( query_embeddings = vectors )
