import json
from gloomhaven_agent.MyAgent import MyAgent

class PredictionGenerator:
    def __init__(self, agent: MyAgent):
        self.agent = agent
        
    def load_dataset(self, file_path: str) -> list[dict]:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def generate_predictions(self, dataset: list[dict]) -> list[dict]:
        predictions = []

        for item in dataset:
            prediction = self.agent.answer(item["question"])

            predictions.append({
                'id': item['id'],
                'question': item['question'],
                'expected_was_played_correctly': item['expected_was_played_correctly'],
                'expected_category': item['expected_category'],
                'prediction': prediction
            })

        return predictions

    def save_predictions(self, predictions: list[dict], output_path: str) -> None:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(predictions, file, indent=2, ensure_ascii=False)

    def run(self, dataset_path: str, output_path: str,) -> list[dict]:
        dataset = self.load_dataset(dataset_path)
        predictions = self.generate_predictions(dataset)
        self.save_predictions(predictions, output_path)
        return predictions