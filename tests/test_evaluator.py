from utils.evaluator import Evaluator
import os
import datetime
from utils.groq_client import GroqClient
from utils.report_generator import ReportGenerator

# Initialize Evaluator
evaluator = Evaluator(threshold=0.85)
groq= GroqClient()

log_dir= os.path.join(os.path.dirname(os.path.dirname(__file__)),'logs')
log_file= os.path.join(log_dir, f"eval_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Load dataset
dataset = evaluator.load_dataset(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset', 'qa_dataset.json')
)

# Run Evaluation
with open(log_file, 'w') as log:

    total = len(dataset)
    passed = 0
    results = []

    for item in dataset:
        qid = item['id']
        question = item['question']
        expected = item['expected_answer']
        actual = groq.ask(question)

        if item["type"] == "hallucination_test":
            score,result = evaluator.is_hallucination_caught(actual)
        else:
            score, result = evaluator.evaluate(actual,expected)

        if result == "PASS":
            passed += 1

        results.append({
            'id': qid,
            'question': question,
            'actual': actual,
            'score': score,
            'result': result,
            'type': item['type']
        })

        line = f"Q{qid}:{question}\nActual: {actual}\nScore: {score} | Result: {result}\n{'-' * 60}\n"
        print(line)
        log.write(line)

    failed = total - passed
    pass_percentage= round((passed/total)*100,2)

    type_summary = {}
    for r in results:
        t = r['type']
        if t not in type_summary:
            type_summary[t] = {'total': 0, 'passed': 0, 'failed': 0}
        type_summary[t]['total'] += 1
        if r['result'] == 'PASS':
            type_summary[t]['passed'] += 1
        else:
            type_summary[t]['failed'] += 1


    summary = f"""
    ==================== SUMMARY ====================
    Total Questions : {total}
    Passed          : {passed}
    Failed          : {failed}
    Pass Percentage : {pass_percentage}%
    =================================================
    """
    print(summary)
    log.write(summary)

    summary= {
        'total': total,
        'passed': passed,
        'failed': failed,
        'pass_percentage': pass_percentage,
        'type_summary': type_summary
    }

    report_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'reports',
        f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )

    reporter = ReportGenerator(results, summary)
    reporter.generate_html(report_path)

print(f"\nLog saved to: {log_file}")

