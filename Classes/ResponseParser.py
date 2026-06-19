import json
import re

class ResponseParser:
    @staticmethod
    def extract_json(text: str) -> dict:
        match = re.search(r"\{.*?\}", text, re.DOTALL)

        if not match:
            return {
                "explanation": text.strip(),
                "was_played_correctly": None,
                "category": None
            }

        json_text = match.group(0)

        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            return {
                "explanation": text.strip(),
                "was_played_correctly": None,
                "category": None
            }