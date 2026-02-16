from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class LangChainLoader:
    def load( self, data_path ):
        document_loader = PyPDFLoader( data_path )
        return document_loader.load()

class LangChainSplitter:
    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
        length_function,
        is_separator_regex: bool
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function
        self.is_separator_regex = is_separator_regex

    def split( self, documents ):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=self.length_function,
            is_separator_regex=self.is_separator_regex,
        )

        return text_splitter.split_documents( documents )
