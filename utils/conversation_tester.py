import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ConversationTester:

    def __init__(self, max_turns=4):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.max_turns = max_turns
        self.conversation_history = []

    def reset(self):
        self.conversation_history = []

    def _add_message(self, role, content):
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def _get_response(self):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "system",
                "content": """
                    You are a helpful customer support assistant. 
                    Answer questions accurately using context from the conversation.
                    If you cannot resolve the issue after multiple attempts say exactly:
                    ESCALATE: I am transferring you to a human agent.
                """

        }] + self.conversation_history
        )
        return response.choices[0].message.content

    def run_conversation(self, turns):
        self.reset()
        results = []
        for i, user_message in enumerate(turns):
            self._add_message('user', user_message)
            response = self._get_response()
            self._add_message('assistant', response)

            escalated = "ESCALATED" in response.upper()

            results.append({
                'turn': i+1,
                'user':user_message,
                'response':response,
                'escalated': escalated
            })

            if escalated:
                break

        final_status= "ESCALATED" if results[-1]['escalated'] else 'RESOLVED'

        return {
            'total_turns': len(results),
            'final_status': final_status,
            'turns': results
        }



