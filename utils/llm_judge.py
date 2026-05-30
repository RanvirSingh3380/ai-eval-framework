import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LLMJudge:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def evaluate(self, question, expected_answer, actual_response):
        prompt = f"""
        You are an expert LLM Judge. Evaluate the following AI model response.
        
        QUESTION: {question}
        EXPECTED_ANSWER: {expected_answer}
        ACTUAL_RESPONSE: {actual_response}
        
        Evaluate using these techniques:
        
        1. CHAIN OF THOUGHTS: Generate your own answer to teh question first.
         Show you reasoning step-by-step. 
         Then compare with the actual response
        2. POSITIONAL BIAS CHECK: Evaluate the actual response based upon its own merit regardless of where it appears.
         Do not favour it just because it is provided.
        3. HUMAN ESCALATION CHECK: Decide if this response is too complex or ambiguous for automation evaluation and
         requre human review
         
        Provide your evaluation in this exact format:
        CHAIN_OF_THOUGHTS: [Your reasoning]
        POSITIONAL_BIAS_RISK: [low/medium/high]
        HUMAN_ESCALATION_NEEDED: [yes/no]
        REASON: [brief explanation]
        VERDICT: [PASS/FAIL]
        """
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

