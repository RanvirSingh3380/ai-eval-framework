import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


class GeminiClient:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def ask(self,question):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question
        )
        return response.text