from langchain_openai import ChatOpenAI

class OpenAILlm:
    openaillm = None

    def __init__( self ):
        self.openaillm = ChatOpenAI( model="gpt-5-nano" )

    def generate_response( self, prompt ):
        response = self.openaillm.invoke([ prompt ])

        return response.text
