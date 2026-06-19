from Classes.ResponseParser import ResponseParser
from abc import ABC, abstractmethod


class BaseRAGEngine(ABC):
    def __init__(self, model):
        self.model = model

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

        Return only a valid JSON object with these keys:
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

    @abstractmethod
    def answer(self, question: str, top_k: int) -> dict:
        pass

    def answer_with_context(self, question: str, context: str) -> dict:
        prompt = self.build_prompt(question, context)
        response = self.model.complete(prompt)
        return ResponseParser.extract_json(response.text)