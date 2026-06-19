from Classes.BaseRAGEngine import BaseRAGEngine
from Classes.WebSearchTool import WebSearchTool

class WebRAGEngine(BaseRAGEngine):
    def __init__(self, model):
        super().__init__(model)

    def build_context(self, web_results: list[dict]) -> str:
        context_parts = []
        for result in web_results:
            title = result.get('title', '')
            href = result.get('href', '')
            body = result.get('body', '')
            context_parts.append(f'Title: {title}\nURL: {href}\n{body}')
        return '\n\n---\n\n'.join(context_parts)

    def answer(self, question: str, top_k: int) -> dict:
        web_results = self.WebSearchTool.search(f'Gloomhaven rules: {question}', max_results=top_k)
        context = self.build_context(web_results)
        answer = self.answer_with_context(question, context)
        answer['source_type'] = 'web'
        answer['sources'] = web_results
        return answer