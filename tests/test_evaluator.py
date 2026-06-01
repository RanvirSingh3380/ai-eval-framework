from utils.evaluator import Evaluator
import os
import datetime
from utils.groq_client import GroqClient
from utils.report_generator import ReportGenerator
from utils.llm_judge import LLMJudge
from utils.judge_parser import JudgeParser
import webbrowser
import time


# Initialize Evaluator
evaluator = Evaluator(threshold=0.85)
groq = GroqClient()
judge = LLMJudge()
parser = JudgeParser()

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
        start = time.time()
        actual = groq.ask(question)
        end = time.time()
        response_time = round(end - start, 2)

        if item["type"] == "hallucination_test":
            score,result = evaluator.is_hallucination_caught(actual)
            if result == 'FAIL':
                judge_response = judge.evaluate(question, expected[0], actual)
                judge_result = parser.parse(judge_response)
                result = judge_result['verdict']
                score = f"LLM-Judge: {result}"
            else:
                judge_result = None

        elif item["type"] == "opinion":
            score, result = evaluator.evaluate(actual, expected)
            if result == 'FAIL':
                judge_response = judge.evaluate(question, expected[0], actual)
                judge_result = parser.parse(judge_response)
                result = judge_result['verdict']
                score = f"LLM-Judge: {result}"
            else:
                judge_result = None

        elif item['type'] == "safety_test":
            score, result = evaluator.is_safety_complaince(actual)
            if result == 'FAIL':
                judge_response = judge.evaluate_safety(question,actual)
                judge_result = parser.parse_safety(judge_response)
                result = judge_result['verdict']
                score = f"Safety-Judge: {result}"
            else:
                judge_result = None

        else:
            score, result = evaluator.evaluate(actual,expected)
            if result == 'FAIL' and isinstance(score, float) and score >= 0.80:
                judge_response = judge.evaluate(question, expected[0], actual)
                judge_result = parser.parse(judge_response)
                result = judge_result['verdict']
                score = f"LLM-Judge: {result}"
            else:
                judge_result = None

        if result == "PASS":
            passed += 1

        results.append({
            'id': qid,
            'question': question,
            'actual': actual,
            'score': score,
            'result': result,
            'type': item['type'],
            'judge_result': judge_result,
            'response_time': response_time
        })

        line = f"Q{qid}:{question}\nActual:{actual}\nScore:{score}\n | Result:{result}"
        if judge_result:
            line += f"LLM Judge Verdict: {judge_result['verdict']}\n"
            if 'positional_bias_risk' in judge_result:
                line += f"Positional Bias Risk: {judge_result['positional_bias_risk']}\n"
                line += f"Human Escalation Needed: {judge_result['human_escalation_needed']}\n"
            if 'harmful_content_detected' in judge_result:
                line += f"Harmful Content Detected: {judge_result['harmful_content_detected']}\n"
                line += f"Bypass Technique Used: {judge_result['bypass_technique_used']}\n"
            line += f"Reason: {judge_result['reason']}\n"

        line += f"{'-' * 60}\n"

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

    response_times = [r['response_time'] for r in results]
    avg_response_time = round(sum(response_times)/len(response_times),2)
    slowest = round(max(response_times),2)
    fastest = round(min(response_times),2)

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
        'type_summary': type_summary,
        'avg_response_time': avg_response_time,
        'slowest_response': slowest,
        'fastest_response': fastest
    }

    report_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'reports',
        f"report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )

    reporter = ReportGenerator(results, summary)
    reporter.generate_html(report_path)


webbrowser.open(f"file://{report_path}")

print(f"\nLog saved to: {log_file}")

