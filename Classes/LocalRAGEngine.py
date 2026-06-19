from Classes.BaseRAGEngine import BaseRAGEngine
from Classes.Retriever import Retriever
from DataClasses.EmbeddedChunk import EmbeddedChunk

class LocalRAGEngine(BaseRAGEngine):
    def __init__(self, retriever: Retriever, model):
        super().__init__(model)
        self.retriever = retriever

    def build_sources(self, retrieved_chunks: list[tuple[EmbeddedChunk, float]]) -> list[dict]:
        sources = []
        for embedded_chunk, score in retrieved_chunks:
            chunk = embedded_chunk.chunk
            sources.append({
                'page_number': chunk.page_number,
                'chunk_number': chunk.chunk_number,
                'score': round(float(score), 3)
            })
        return sources

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
        answer['sources'] = self.build_sources(retrieved_chunks)
        best_score = retrieved_chunks[0][1] if retrieved_chunks else 0.0
        best_score = round(float(best_score), 3)
        answer['best_retrieval_score'] = best_score
        return answer