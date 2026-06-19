from dataclasses import dataclass
from DataClasses.Chunk import Chunk

@dataclass
class EmbeddedChunk:
    chunk: Chunk
    embedding: list[float]