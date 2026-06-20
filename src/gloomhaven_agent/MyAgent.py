from gloomhaven_agent.rag.BaseRAGEngine import BaseRAGEngine
from gloomhaven_agent.rag.LocalRAGEngine import LocalRAGEngine
from gloomhaven_agent.rag.WebRAGEngine import WebRAGEngine

class MyAgent:
    def __init__(self, local_rag_engine: LocalRAGEngine,
                 web_rag_engine: WebRAGEngine,
                 retrieval_threshold: float,
                 local_top_k: int,
                 web_top_k: int):
        self.local_rag_engine = local_rag_engine
        self.web_rag_engine = web_rag_engine
        self.retrieval_threshold = retrieval_threshold
        self.local_top_k = local_top_k
        self.web_top_k = web_top_k
        self.fallback_explanation_keywords = ['not found','no relevant information',
                                              'insufficient information', 'unable to find',
                                              'not available']
        self.web_keywords = ['reddit', 'community', 'forum', 'designer', 'interview',
                             'opinion', 'consensus', 'online', 'discussion', 'players think']

    def fallback(self, local_answer: dict) -> bool:
        best_score = local_answer.get('best_retrieval_score', 0.0)
        explanation = local_answer.get('explanation', '').lower()
        played_correctly = local_answer.get('was_played_correctly', None)
        if best_score < self.retrieval_threshold:
            return True
        if played_correctly is None:
            return True
        if any(keyword in explanation for keyword in self.fallback_explanation_keywords):
            return True
        return False

    def answer(self, question: str) -> dict:
        local_answer = ''
        if not any(keyword in question for keyword in self.web_keywords):
            local_answer = self.local_rag_engine.answer(question, self.local_top_k)
            if not self.fallback(local_answer):
                return local_answer
        web_answer = self.web_rag_engine.answer(question, self.web_top_k)
        web_answer['fallback_reason'] = 'Local retrieval insufficient, falling back to web search.'
        web_answer['local_answer'] = local_answer
        return web_answer

