from utils.ensemble_judge import EnsembleJudge

judge= EnsembleJudge(num_judges=3)

result = judge.evaluator(
        question="What is the capital of France?",
        expected_answer="The capital of France is Paris.",
        actual_response="The capital of France is London."
)

print(f"Individual Votes: {result['individual_votes']}")
print(f"Pass Count: {result['pass_count']}")
print(f"Fail Count: {result['fail_count']}")
print(f"Final Verdict: {result['final_verdict']}")
print("\nReasons:")
for reason in result['reasons']:
    print(f"  {reason}")