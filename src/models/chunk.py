from dataclasses import dataclass, field

@dataclass
class Chunk:
    """A piece of a document returned by a similarity search."""
    text: str
    metadata: dict = field( default_factory = dict )
