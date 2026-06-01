from utils.consistency_checker import ConsistencyChecker
from utils.groq_client import GroqClient

groq = GroqClient()
checker = ConsistencyChecker()

# Test factual question
print("=== Factual Question ===")
result = checker.check("What is the capital of France?", groq, runs=3)
print(f"Avg Consistency: {result['avg_consistency']}")
print(f"Consistent: {result['consistent']}")
print(f"Pairwise Scores: {result['pairwise_scores']}")

print("\n=== Opinion Question ===")
result2 = checker.check("Will AI replace human jobs?", groq, runs=3)
print(f"Avg Consistency: {result2['avg_consistency']}")
print(f"Consistent: {result2['consistent']}")
print(f"Pairwise Scores: {result2['pairwise_scores']}")