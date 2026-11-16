from pydantic import BaseModel

class AskRequest( BaseModel ):
    question: str

class Source( BaseModel ):
    filename: str
    page: int | None = None

class AskResponse( BaseModel ):
    answer: str
    sources: list[ Source ]
