from langchain_openai import OpenAIEmbeddings

class OpenAIEmbedding:
    openai_embeddings = None

    def __init__( self, model = "text-embedding-3-large", dimensions = 1024 ):
        self.openai_embeddings = OpenAIEmbeddings(
            model = model,
            dimensions = dimensions
        )

    def embed_documents( self, documents ):
        vectors = self.openai_embeddings.embed_documents( documents )
        return vectors

    def embed_query( self, query ):
        vector = self.openai_embeddings.embed_query( query )
        return vector
