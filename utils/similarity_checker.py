from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer('all-MiniLM-L6-v2')

sentence1 = "The capital of france is Paris"
sentence2 = "Paris is the capital of France"

embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)

score = util.cos_sim(embedding1,embedding2)

print(f"Similarity Score: {score.item():.4f}")