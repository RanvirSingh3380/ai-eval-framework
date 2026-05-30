class JudgeParser:

    def parse(self, judge_response):
        result= {
            'chain_of_thoughts': '',
            'positional_bias_risk': '',
            'human_escalation_needed': '',
            'reason': '',
            'verdict': 'FAIL'
        }

        lines = judge_response.strip().split('\n')
        for line in lines:
            if line.startswith('CHAIN_OF_THOUGHTS:'):
                result['chain_of_thoughts'] = line.replace('CHAIN_OF_THOUGHTS:', '').strip()
            elif line.startswith('POSITIONAL_BIAS_RISK:'):
                result['positional_bias_risk'] = line.replace('POSITIONAL_BIAS_RISK:', '').strip()
            elif line.startswith('HUMAN_ESCALATION_NEEDED:'):
                result['human_escalation_needed'] = line.replace('HUMAN_ESCALATION_NEEDED:', '').strip()
            elif line.startswith('REASON:'):
                result['reason'] = line.replace('REASON:', '').strip()
            elif line.startswith('VERDICT:'):
                verdict = line.replace('VERDICT:', '').strip()
                result['verdict'] = 'PASS' if 'PASS' in verdict.upper() else 'FAIL'

        return result





