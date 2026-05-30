class ReportGenerator:
    def __init__(self, results, summary):
        self.results = results
        self.summary = summary

    def generate_html(self, output_path):
        rows = ""

        for r in self.results:
            color = "#2ecc71" if r['result'] == "PASS" else "#e74c3c"
            actual_display = r['actual'][:300] + '...' if len(r['actual']) > 300 else r['actual']

            judge_info = ""
            if r.get('judge_result'):
                jr = r['judge_result']
                judge_info = f"""
                    <b>Verdict:</b> {jr['verdict']}<br>
                    <b>Bias Risk:</b> {jr['positional_bias_risk']}<br>
                    <b>Escalation:</b> {jr['human_escalation_needed']}<br>
                    <b>Reason:</b> {jr['reason']}
                    """

            rows += f"""
            <tr>
                <td>{r['id']}</td>
                <td>{r['question']}</td>
                <td>{actual_display}</td>
                <td>{r['score']}</td>
                <td style="background-color:{color}; color:white; font-weight:bold;">{r['result']}</td>
                <td>{judge_info}</td>
            </tr>
            """

        html = f"""
        <html>
        <head>
            <title>AI Eval Report</title>
            <style>
                body {{ font-family: Arial; padding: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ background-color: #2c3e50; color: white; padding: 10px; }}
                td {{ border: 1px solid #ddd; padding: 8px; vertical-align: top; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .summary {{ background-color: #2c3e50; color: white; 
                            padding: 15px; margin-bottom: 20px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>AI Evaluation Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total: {self.summary['total']} | 
                   Passed: {self.summary['passed']} | 
                   Failed: {self.summary['failed']} | 
                   Pass Rate: {self.summary['pass_percentage']}%
                </p>
            <table style="color:white; margin-top:10px; width:50%;">
                <tr>
                    <th style="text-align:left;">Type</th>
                    <th>Total</th>
                    <th>Passed</th>
                    <th>Failed</th>
                </tr>
                {''.join([f"""
                <tr>
                    <td>{t}</td>
                    <td style="text-align:center;">{v['total']}</td>
                    <td style="text-align:center; color:#2ecc71;">{v['passed']}</td>
                    <td style="text-align:center; color:#e74c3c;">{v['failed']}</td>
                </tr>
                """ for t, v in self.summary['type_summary'].items()])}
            </table>
            </div>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Question</th>
                    <th>Actual Response</th>
                    <th>Score</th>
                    <th>Result</th>
                    <th>Judge Details</th>
                </tr>
                {rows}
            </table>
        </body>
        </html>
        """

        with open(output_path, 'w') as f:
            f.write(html)
        print(f"HTML Report saved to: {output_path}")