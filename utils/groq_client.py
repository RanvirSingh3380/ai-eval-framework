import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqClient:

    def __init__(self):
        api_key= os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def ask(self,question):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return response.choices[0].message.content

