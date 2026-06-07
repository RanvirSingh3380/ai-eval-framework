import os
import time
from groq import Groq
from dotenv import load_dotenv
from utils.evaluator import Evaluator

load_dotenv()


class ModelComparator:

    def __init__(self, model_a, model_b, threshold=0.85):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_a = model_a
        self.model_b = model_b
        self.evaluator = Evaluator(threshold=threshold)

    def _ask(self, model, question):
        start = time.time()
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}]
        )
        end = time.time()
        return{
            'response': response.choices[0].message.content,
            'response_time': round(end-start,2)
        }

    def compare(self, questions):
        results = []

        for item in questions:
            question = item['question']
            expected = item.get('expected_answer', [])

            result_a = self._ask(self.model_a, question)
            result_b = self._ask(self.model_b, question)

            if item.get('type') == 'hallucination_test':
                score_a, verdict_a = self.evaluator.is_hallucination_caught(result_a['response'])
                score_b, verdict_b = self.evaluator.is_hallucination_caught(result_b['response'])
            elif item.get('type') == 'safety_test':
                score_a, verdict_a = self.evaluator.is_safety_complaince(result_a['response'])
                score_b,verdict_b = self.evaluator.is_safety_complaince(result_b['response'])
            else:
                score_a, verdict_a = self.evaluator.evaluate(
                    result_a['response'], expected
                ) if expected else (None, 'N/A')

                score_b, verdict_b = self.evaluator.evaluate(
                    result_b['response'], expected
                ) if expected else (None, 'N/A')

            results.append({
                'question': question,
                'type': item.get('type', 'factual'),
                'model_a': {
                    'name': self.model_a,
                    'response': result_a['response'],
                    'response_time': result_a['response_time'],
                    'score': score_a,
                    'verdict': verdict_a
                },
                'model_b':{
                    'name': self.model_b,
                    'response': result_b['response'],
                    'response_time': result_b['response_time'],
                    'score': score_b,
                    'verdict': verdict_b
                }
            })
        return results

    def generate_summary(self, results):
        total = len(results)
        avg_time_a = round(sum(r['model_a']['response_time'] for r in results) / total, 2)
        avg_time_b = round(sum(r['model_b']['response_time'] for r in results) / total, 2)

        faster_model = self.model_a if avg_time_a < avg_time_b else self.model_b

        passes_a = sum(1 for r in results if r['model_a']['verdict'] == 'PASS')
        passes_b = sum(1 for r in results if r['model_b']['verdict'] == 'PASS')
        better_quality = self.model_a if passes_a >= passes_b else self.model_b

        return {
            'total_questions': total,
            'model_a': self.model_a,
            'model_b': self.model_b,
            'avg_response_time_a': avg_time_a,
            'avg_response_time_b': avg_time_b,
            'faster_model': faster_model,
            'passes_a': passes_a,
            'passes_b': passes_b,
            'better_quality': better_quality
        }