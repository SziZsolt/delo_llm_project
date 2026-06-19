from llama_index.llms.huggingface import HuggingFaceLLM

class ModelBuilder:
    @staticmethod
    def build_model(model_name: str) -> HuggingFaceLLM:
        model = HuggingFaceLLM(
            model_name=model_name,
            tokenizer_name=model_name,
        )
        return model