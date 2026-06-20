from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

class ModelBuilder:
    @staticmethod
    def build_llm(model_name: str) -> HuggingFaceLLM:
        model = HuggingFaceLLM(model_name=model_name, tokenizer_name=model_name)
        return model
    
    @staticmethod
    def build_embedder(model_name: str) -> HuggingFaceEmbedding:
        embedder = HuggingFaceEmbedding(model_name=model_name)
        return embedder