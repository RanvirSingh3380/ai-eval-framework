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
```
ai_eval_framework/
├── dataset/          # Golden Q&A dataset
├── tests/            # Test scripts
├── utils/            # Evaluator, Groq client, Report generator
├── reports/          # HTML evaluation reports
├── logs/             # Text log files
└── screenshots/      # Evidence screenshots
```

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

## Data Generation
Synthatic test datasets can be auto-generated from raw text or articles using built-in DataGenerator
- Automatically creates factual, opinion and hallucination_test questions
- Output follows the same JSON structure as the evaluation dataset
- Plug n Play - generate datasets work directly with the evaluation framework
  
Run: `python test_data_generator.py`

## Design Decisions
- **Groq API** - Used for evaluation and data generation. Fast, free tier, no data storage.
- **Offline option** - Ollama with Mistral 7B planned for privacy-first environments requiring 16GB+ RAM.
- **Sentence Transformers** — Chosen for offline semantic similarity scoring without API dependency.
- **LLM-as-Judge** — Added for opinion and complex questions where semantic similarity alone is insufficient.

## Planned Enhancements
- JMeter load testing — concurrent user simulation for AI API endpoints
- Ollama offline integration — privacy-first data generation for 16GB+ RAM machines
- Ensemble voting — panel of LLM judges for complex evaluation

## Author
Ranvir Singh - QA Manager transitioning to AI Quality Engineering 
