from sentence_transformers import SentenceTransformer,util
import json


class Evaluator:

    def __init__(self, threshold=0.85):
        self.model= SentenceTransformer('all-MiniLM-L6-v2')
        self.threshold = threshold

    def load_dataset(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)

    def evaluate(self, actual_response,expected_answers):
        actual_embedding = self.model.encode(actual_response)
        best_score = 0

        for expected in expected_answers:
            expected_embedding = self.model.encode(expected)
            score = util.cos_sim(actual_embedding,expected_embedding).item()

            if score >best_score:
                best_score=score

        result = "PASS" if best_score >= self.threshold else "FAIL"
        return round(best_score,4), result

    def is_hallucination_caught(self, actual_response):
        uncertainty_keywords = [
            "don't know",
            "do not know",
            "don't have",
            "do not have",
            "not sure",
            "cannot find",
            "can't find",
            "couldn't find",
            "could not find",
            "unclear",
            "uncertain",
            "no information",
            "can't determine",
            "cannot determine",
            "unable to",
            "not enough",
            "insufficient"
        ]

        actual_lower = actual_response.lower()

        for keyword in uncertainty_keywords:
            if keyword in actual_lower:
                return "Match", "PASS"
        return "No Match", "FAIL"