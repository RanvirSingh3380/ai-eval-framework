# Note: Ideal ensemble uses models from different families/providers
# to reduce shared training bias. Current implementation uses Groq
# free tier models. Production should mix providers (OpenAI, Anthropic, Google).


import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class EnsembleJudge:

    def __init__(self, num_judges=3):
        self. client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.num_judges = num_judges
        self.model = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "qwen/qwen3-32b"
        ]

    def get_judge_prompt(self, question, expected_answer, actual_response):
        return f""" You are an expert AI response evaluator.
        
        Question: {question}
        Expected Answer: {expected_answer}
        Actual Response: {actual_response}
        
        Evaluate if the actual response correctly and sufficiently answers the question compared to the expected answer.
        
        Consider:
        1. Factual accuracy
        2. Completeness
        3. Relevance
        
        Respond in this EXACT format:
        VERDICT: [PASS/FAIL]
        REASON: [one line explanation]      
        """

    def evaluator(self, question, expected_answer, actual_response):
        votes = []
        reasons = []

        for i, model in enumerate(self.model[:self.num_judges]):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{
                        'role': 'user',
                        'content': self.get_judge_prompt(question, expected_answer, actual_response)
                    }]
                )

                raw = response.choices[0].message.content
                verdict = "PASS" if "VERDICT: PASS" in raw.upper() else "FAIL"
                votes.append(verdict)

                for line in raw.split('\n'):
                    if line.upper().startswith('REASON:'):
                        reasons.append(f"Judge {i + 1}: {line.split(':', 1)[1].strip()}")

            except Exception as e:
                votes.append("FAIL")
                reasons.append(f"Judge {i+1}: Error - {str(e)}")

        pass_votes = votes.count("PASS")
        fail_votes = votes.count("FAIL")
        final_verdict = "PASS" if pass_votes > fail_votes else "FAIL"

        return {
            'individual_votes': votes,
            'pass_count': pass_votes,
            'fail_count': fail_votes,
            'final_verdict': final_verdict,
            'reasons': reasons
        }




