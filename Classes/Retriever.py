from Classes.EmbeddingStore import EmbeddingStore
import numpy as np
from DataClasses.EmbeddedChunk import EmbeddedChunk

class Retriever:
    def __init__(self, embedding_store: EmbeddingStore, embed_model):
        self.embedding_store = embedding_store
        self.embed_model = embed_model

    def cosine_similarity(self, arr_1: np.ndarray, arr_2: np.ndarray) -> float:
        arr_1 = np.asarray(arr_1)
        arr_2 = np.asarray(arr_2)
        dot_product = np.dot(arr_1, arr_2)
        norm_arr_1 = np.linalg.norm(arr_1)
        norm_arr_2 = np.linalg.norm(arr_2)
        denom = norm_arr_1 * norm_arr_2
        if denom == 0:
            return 0.0
        cos_sim = dot_product / denom
        if np.isnan(cos_sim) or np.isinf(cos_sim):
            return 0.0
        return float(cos_sim)

    def retrieve(self, query: str, top_k: int) -> list[tuple[EmbeddedChunk, float]]:
        query_embedding = self.embed_model.get_text_embedding(query)
        embedded_chunks = self.embedding_store.get_embedded_chunks()

        similarities = [
            (chunk, self.cosine_similarity(query_embedding, chunk.embedding))
            for chunk in embedded_chunks
        ]

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
