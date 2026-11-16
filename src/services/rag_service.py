class RagService:
    llmService = None
    embeddingService = None
    vectorStore = None

    def __init__( self, llmService, embeddingService, vectorStore ):
        self.llmService = llmService
        self.embeddingService = embeddingService
        self.vectorStore = vectorStore

    def ask( self, question ):
        embedding = self.embeddingService.embed_query( question )

        chunks = self.vectorStore.similarity_search( embedding )

        prompt = self.llmService.build_prompt( question, [ chunk.text for chunk in chunks ] )

        answer = self.llmService.generate_response( prompt )

        return answer, chunks
