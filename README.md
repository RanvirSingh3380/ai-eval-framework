# AI Evaluation Framework

An automated AI model evaluation framework built with python to assess LLm response quality at scale.

## What it does
- Evaluate AI model response against a golden dataset
- Uses semantic similarity scoring for factual questions
- Detect hallucination using keyword-based uncertainty matching
- Generates professional HTML report with pass/fail results
- Logs every evaluation run with timestamps

# Tech Stack
- Python 3.12
- Sentence Transformers (Hugging Face)
- Groq API (LLaMA 3.3)
- Python-dotenv
- Playwright

## Project Structure
ai_eval_framework/
├── dataset/          # Golden Q&A dataset
├── tests/            # Test scripts
├── utils/            # Evaluator, Groq client, Report generator
├── reports/          # HTML evaluation reports
├── logs/             # Text log files
└── screenshots/      # Evidence screenshots

## Setup
1. Clone the repository
2. Create Virtual environment: 'python3 -m venv .venv'
3. Activate: 'source .venv/bin/activate'
4. Install dependencies: 'pip install -r requirements.txt'
5. Create '.env' fill with your 'GROQ_API_KEY'
6. Run 'python tests/test_evaluator.py'

## Evaluation Layer
1. **Layer 1** - Semantic similarity scoring with 0.85 threshold
2. **Layer 2** - Hallucination detected via uncertainty keyword matching
3. **Layer 3** - LLM-as-Judge *(coming soon)*

## Author
Ranvir Singh - QA Manager transitioning to AI Quality Engineering 