import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class DataGenerator:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_from_text(self, raw_text, num_questions=10):
        prompt = f"""
        You are an expert at creating Q&A datasets for AI model evaluation.

        Read the following text carefully and generate exactly {num_questions} questions and answers.

        Mix of question types:
        - 6 factual questions (clear correct answers from the text, expected answers should be detailed and descriptive, at least 2-3 sentences)
        - 2 opinion questions (open-ended, multiple valid answers)
        - 2 hallucination_test questions (ask about something NOT in the text)

        TEXT:
        {raw_text}

        Return ONLY a valid JSON array in this exact format, no extra text:
        [
        {{
            "id": 1,
            "question": "question here",
            "expected_answer": ["answer here"],
            "type": "factual"
        }}
        ]

        For opinion questions include 2-3 expected answers.
        For hallucination_test questions set expected_answer to ["I don't know", "I don't have information about that."]
        """
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_response = response.choices[0].message.content
        clean = raw_response.strip()
        if clean.startswith("```"):
           clean = clean.split("```")[1]
           if clean.startswith("json"):
               clean = clean[4:]
        clean = clean.strip()

        return json.loads(clean)

    def save_dataset(self, questions, output_path):
        with open(output_path, 'w') as f:
            json.dump(questions, f, indent=2)
            print(f"Dataset saved to: {output_path}")