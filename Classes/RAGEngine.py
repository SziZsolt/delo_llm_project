from Classes.Retriever import Retriever
from Classes.ResponseParser import ResponseParser
from DataClasses.EmbeddedChunk import EmbeddedChunk

class RAGEngine:
    def __init__(self, retriever: Retriever, model):
        self.retriever = retriever
        self.model = model

    def build_context(self, retrieved_chunks) -> str:
        context_parts = []
        for embedded_chunk, score in retrieved_chunks:
            chunk = embedded_chunk.chunk
            context_parts.append(
                f'[Page {chunk.page_number}, Chunk {chunk.chunk_number}, Score {score:.3f}]\n'
                f'{chunk.text}'
            )
        return "\n\n---\n\n".join(context_parts)
    
    def build_sources(self, retrieved_chunks: list[tuple[EmbeddedChunk, float]]) -> list[dict]:
        sources = []
        for embedded_chunk, score in retrieved_chunks:
            chunk = embedded_chunk.chunk
            sources.append({
                'page_number': chunk.page_number,
                'chunk_number': chunk.chunk_number,
                'score': score
            })
        return sources

    def build_prompt(self, question: str, context: str) -> str:
        return f'''
        You are a Gloomhaven board game rules assistant.

        Use only the rulebook context below.

        Your task:
        - Decide whether the user handled the situation correctly.
        - Explain the relevant rule briefly.
        - Assign exactly one category.

        Allowed categories:
        BoardGameSetup, Combat, Scenario, Character

        Return ONLY a valid JSON object with these keys:
        explanation: string
        was_played_correctly: boolean
        category: one of the allowed categories

        Do not include markdown.
        Do not include text before or after the JSON.

        Rulebook context:
        {context}

        User question:
        {question}

        JSON:
        '''

    def answer(self, question: str, top_k: int) -> str:
        retrieved_chunks = self.retriever.retrieve(question, top_k=top_k)
        context = self.build_context(retrieved_chunks)
        prompt = self.build_prompt(question, context)
        response = self.model.complete(prompt)
        parsed_response = ResponseParser.extract_json(response.text)
        parsed_response['sources'] = self.build_sources(retrieved_chunks)
        return parsed_response