from Classes.DocumentProcessing.Chunker import Chunker
from DataClasses.EmbeddedChunk import EmbeddedChunk

class EmbeddingStore:
    def __init__(self, chunker: Chunker, embed_model):
        self.chunker = chunker
        self.embed_model = embed_model
        self.embedded_chunks = self.embed_chunks()

    def embed_chunks(self) -> list[EmbeddedChunk]:
        embedded_chunks = []
        for chunk in self.chunker.get_chunks():
            embedding = self.embed_model.get_text_embedding(chunk.text)
            embedded_chunks.append(EmbeddedChunk(chunk=chunk, embedding=embedding))
        return embedded_chunks
    
    def get_embedded_chunks(self) -> list[EmbeddedChunk]:
        return self.embedded_chunks