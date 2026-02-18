class RagService:
    llmService = None
    embeddingService = None
    vectorStore = None

    def __init__( self, llmService, embeddingService, vectorStore ):
        self.llmService = llmService
        self.embeddingService = embeddingService
        self.vectorStore = vectorStore

    def ask( self, message ):
        embedding = self.embeddingService.embed_query( message )

        chunks = self.vectorStore.similarity_search( [ embedding ] )

        prompt = self.llmService.build_prompt( message, chunks )

        response = self.llmService.generate_response( prompt )

        return response
