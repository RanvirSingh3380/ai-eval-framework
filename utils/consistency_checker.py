from sentence_transformers import SentenceTransformer, util


class ConsistencyChecker:

    def __init__(self,):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def check(self, question, groq_client, runs=3):
        responses = []
        for i in range(runs):
            response = groq_client.ask(question)
            responses.append(response)

        scores = []
        for i in range(len(responses)):
            for j in range(i + 1, len(responses)):
                embedding1 = self.model.encode(responses[i])
                embedding2 = self.model.encode(responses[j])
                score = util.cos_sim(embedding1, embedding2).item()
                scores.append(round(score, 4))

        average_consistency = round(sum(scores) / len(scores), 4)
        return {
            'question': question,
            'runs': runs,
            'responses': responses,
            'pairwise_scores': scores,
            'avg_consistency': average_consistency,
            'consistent': average_consistency >= 0.85
        }



