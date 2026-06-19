from Classes.BaseRAGEngine import BaseRAGEngine
from Classes.Retriever import Retriever
from DataClasses.EmbeddedChunk import EmbeddedChunk

class LocalRAGEngine(BaseRAGEngine):
    def __init__(self, retriever: Retriever, model):
        super().__init__(model)
        self.retriever = retriever

    def build_context(self, retrieved_chunks: list[tuple[EmbeddedChunk, float]]) -> str:
        context_parts = []
        for embedded_chunk, score in retrieved_chunks:
            chunk = embedded_chunk.chunk
            page_number = chunk.page_number
            chunk_number = chunk.chunk_number
            context_parts.append(f'[Page: {page_number}, Chunk: {chunk_number}, Score: {score:.3f}]\n{chunk.text}')
        return '\n\n---\n\n'.join(context_parts)

    def answer(self, question: str, top_k: int) -> dict:
        retrieved_chunks = self.retriever.retrieve(question, top_k)
        context = self.build_context(retrieved_chunks)
        answer = self.answer_with_context(question, context)
        answer['source_type'] = 'rulebook'
        return answer