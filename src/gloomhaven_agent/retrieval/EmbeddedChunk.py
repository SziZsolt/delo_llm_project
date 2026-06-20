from dataclasses import dataclass
from gloomhaven_agent.document_processing.Chunk import Chunk

@dataclass
class EmbeddedChunk:
    chunk: Chunk
    embedding: list[float]