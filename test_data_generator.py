from utils.data_generator import DataGenerator

generator = DataGenerator()

# Sample article text
sample_text = """
Artificial Intelligence (AI) is transforming the world in many ways. 
Machine learning, a subset of AI, allows computers to learn from data without being explicitly programmed.
Deep learning uses neural networks with many layers to process complex patterns.
AI is being used in healthcare to diagnose diseases, in finance to detect fraud, 
and in transportation for self-driving cars.
The global AI market is expected to reach $1.8 trillion by 2030.
Some experts worry about job displacement due to AI automation.
Others believe AI will create more jobs than it eliminates.
"""

questions = generator.generate_from_text(sample_text)

for q in questions:
    print(f"ID: {q['id']}")
    print(f"Type: {q['type']}")
    print(f"Question: {q['question']}")
    print(f"Expected: {q['expected_answer']}")
    print(("-" * 50))

generator.save_dataset(questions,'dataset/generated_dataset.json')

print("\n-----------Testing Excel Integration------------")
excel_questions = generator.generate_from_excel(
'dataset/test_data.xlsx',
    column_name='content',
    num_questions=10
)

for q in excel_questions:
    print(f"ID: {q['id']}")
    print(f"Type: {q['type']}")
    print(f"Question: {q['question']}")
    print(("-" * 50))

generator.save_dataset(excel_questions, 'dataset/excel_generated_dataset.json')

