class LlmService:
    llmProvider = None
    promptTemplate = None

    def __init__( self, llmProvider, promptTemplate ):
        self.llmProvider = llmProvider
        self.promptTemplate = promptTemplate

    def build_prompt( self, message, chunk_texts ):
        context = "\n\n".join( chunk_texts )
        return self.promptTemplate.format( question = message, context = context )

    def generate_response( self, prompt ):
        return self.llmProvider.generate_response( prompt )
