# AI Evaluation Framework
An automated AI model evaluation framework built with Python to assess LLM response quality at scale.

## What it does
- Evaluate AI model responses against a golden dataset
- Semantic similarity scoring for factual questions
- Hallucination detection using keyword-based uncertainty matching
- Red teaming and safety testing with bypass detection
- Ensemble voting using panel of 3 LLM judges
- Multi-turn conversation context testing
- Response time tracking and performance metrics
- Bias detection — confirmation bias and myth correction testing
- Prompt injection testing with bypass detection
- Model comparison — side by side evaluation of two LLMs
- Consistency testing — pairwise scoring across multiple runs
- Auto generates test datasets from text or Excel files
- REST API endpoint via Flask for external integrations
- Load testing support via JMeter test plan
- CI/CD pipeline via GitHub Actions
- Generates professional HTML report with pass/fail results
- Logs every evaluation run with timestamps

## Tech Stack
- Python 3.12
- Sentence Transformers (Hugging Face)
- Groq API (LLaMA 3.3, LLaMA 3.1, Qwen3)
- Flask — REST API wrapper
- JMeter — Load testing
- Python-dotenv
- openpyxl — Excel data ingestion
- GitHub Actions — CI/CD pipeline

## Project Structure
```
ai_eval_framework/
├── .github/workflows/    # CI/CD pipeline
├── dataset/              # Golden Q&A dataset
├── tests/                # Test scripts
├── utils/                # Evaluator, Groq client, Report generator
├── app.py                # Flask REST API
├── ai_load_test.jmx      # JMeter load test plan
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

## Setup
1. Clone the repository
2. Create virtual environment: `python3 -m venv .venv`
3. Activate: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with your `GROQ_API_KEY`
6. Run: `python tests/test_evaluator.py`

## REST API
Start the Flask API server:
`python app.py`

Endpoints:
- `GET /health` — Check API status
- `POST /evaluate` — Evaluate a question against expected answer

Example request:
```json
{
  "question": "What is the capital of France?",
  "expected_answers": ["The capital of France is Paris."]
}
```

## Load Testing
Open `ai_load_test.jmx` in JMeter to run load tests against the Flask API.
Results: 10 concurrent users, 0% error rate, 555ms average response time.

## Evaluation Layers
1. **Layer 1** — Semantic similarity scoring with 0.85 threshold
2. **Layer 2** — Hallucination detection via uncertainty keyword matching
3. **Layer 3** — LLM-as-Judge with chain of thought, bias mitigation and ensemble voting
4. **Layer 4** — Red teaming and safety testing with bypass detection

## Dataset Types
- `factual` — Clear correct answers
- `opinion` — Open ended, multiple valid answers
- `hallucination_test` — Questions model cannot know
- `safety_test` — Harmful content refusal testing
- `bias_test` — Confirmation bias detection
- `prompt_injection` — Injection attack testing

## Data Generation
Synthetic test datasets auto-generated from raw text or Excel files.
Run: `python test_data_generator.py`

## Design Decisions
- **Groq API** — Fast, free tier, no data storage
- **Sentence Transformers** — Offline semantic scoring, no API dependency
- **LLM-as-Judge** — For opinion and complex questions where similarity scoring is insufficient
- **Ensemble Voting** — 3 independent judges reduce single model bias
- **Flask API** — Enables JMeter load testing and external integrations
- **Cloud Deployment** — GitHub Actions CI/CD pipeline runs full evaluation on every push
- **Offline option** — Ollama with Mistral 7B planned for 16GB+ RAM environments

## Planned Enhancements
- Ollama offline integration — privacy-first data generation
- Ensemble voting with cross-provider judges (OpenAI + Anthropic + Google)
- Real time evaluation dashboard

## Author
Ranvir Singh — AI Quality Engineering Leader | Building production-grade LLM testing systems
GitHub: github.com/RanvirSingh3380
LinkedIn: linkedin.com/in/ranvir-singh-test-engineer44
