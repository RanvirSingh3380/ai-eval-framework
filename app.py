from flask import Flask, request, jsonify


from utils.evaluator import Evaluator
from utils.groq_client import GroqClient

app = Flask(__name__)

evaluator = Evaluator(threshold=0.85)
groq = GroqClient()


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message':'AI Evaluation API is running'})


@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json

    if not data or 'question' not in data:
        return jsonify({'error': 'question field is required'}), 400

    question = data['question']
    expected_answers = data.get('expected_answers', [])

    actual = groq.ask(question)

    if expected_answers:
        score, result = evaluator.evaluate(actual, expected_answers)

    else:
        score = None
        result = 'NO_EXPECTED_ANSWER'

    return {
        'question': question,
        'actual_response': actual,
        'score': score,
        'result': result
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)


















