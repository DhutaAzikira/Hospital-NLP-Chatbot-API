from sentence_transformers import SentenceTransformer, util
from intent_dictionary import intent_dictionary

class IntentClassifier:
    def __init__(self):
        self.model = SentenceTransformer('./models/all-MiniLM-L6-v2')
        self.intents = intent_dictionary
        # Flatten the intents and compute embeddings
        self.intent_phrases = [phrase for phrases in self.intents.values() for phrase in phrases]
        self.embeddings = self.model.encode(self.intent_phrases, convert_to_tensor=True)

    def classify(self, user_input: str) -> str:
        input_emb = self.model.encode(user_input, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(input_emb, self.embeddings)[0]
        best_match_idx = scores.argmax().item()
        best_score = scores[best_match_idx].item()

        # Set a similarity threshold
        if best_score < 0.4:  # Adjust the threshold as needed
            return "fallback"

        # Map index back to intent
        intent_idx = 0
        for i, phrases in enumerate(self.intents.values()):
            if best_match_idx < len(phrases):
                intent_idx = i
                break
            best_match_idx -= len(phrases)

        return list(self.intents.keys())[intent_idx]

intent_classifier = IntentClassifier()