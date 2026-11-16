from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.dependencies import get_embedding, get_llm_provider, get_vector_store, get_file_storage
from src.infrastructure import ChromaVectorStore, LocalFileStorage

FIXTURES_DIR = Path( __file__ ).parent / "fixtures"


class FakeEmbedding:
    """Deterministic stand-in for OpenAIEmbedding: counts letters a-z.

    Texts that share words end up close together, which is enough for
    Chroma's similarity search to behave sensibly in tests.
    """

    def _embed( self, text ):
        text = text.lower()
        return [ float( text.count( letter ) ) for letter in "abcdefghijklmnopqrstuvwxyz" ]

    def embed_documents( self, documents ):
        return [ self._embed( document ) for document in documents ]

    def embed_query( self, query ):
        return self._embed( query )


class FakeLlm:
    """Stand-in for OpenAILlm that records the prompt it was given."""

    def __init__( self ):
        self.prompts = []

    def generate_response( self, prompt ):
        self.prompts.append( prompt )
        return "fake answer"


@pytest.fixture
def fake_llm():
    return FakeLlm()


@pytest.fixture
def client( tmp_path, fake_llm ):
    # A fresh collection per test so tests do not see each other's chunks.
    vector_store = ChromaVectorStore( collection_name = f"test-{uuid4()}" )

    app.dependency_overrides[ get_embedding ] = lambda: FakeEmbedding()
    app.dependency_overrides[ get_llm_provider ] = lambda: fake_llm
    app.dependency_overrides[ get_vector_store ] = lambda: vector_store
    app.dependency_overrides[ get_file_storage ] = lambda: LocalFileStorage( base_dir = tmp_path )

    yield TestClient( app )

    app.dependency_overrides.clear()


@pytest.fixture
def sample_pdf():
    return ( FIXTURES_DIR / "sample.pdf" ).read_bytes()
