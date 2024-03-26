import numpy as np
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity

WEIGHT = 0.3

class RecommendationByKeywordsCosine:
    def initialize(self, documents):
        self.documents = documents
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        self.weight = WEIGHT

    def prepare_data(self, new_keywords):
        keywords_by_document = self.documents.get_keywords_by_document()
        
        embeddings_keywords_by_document = []
        
        # Convert keywords to a single string
        new_keywords_combined = ' '.join(new_keywords)
        embeddings_new_keywords = self.embed([new_keywords_combined])

        # Obtain vector representations for the keywords of each document
        for document_keywords in keywords_by_document.values():
            document_keywords_combined = ' '.join(document_keywords)
            embeddings_keywords_by_document.append(self.embed([document_keywords_combined]))

        embeddings_keywords_by_document = np.array(embeddings_keywords_by_document)
        
        # Compute cosine similarity between vector representations of document keywords and new keywords
        similarities = cosine_similarity(embeddings_keywords_by_document.reshape(len(embeddings_keywords_by_document), -1), embeddings_new_keywords)

        return similarities.flatten()

    def get_recommendations(self, document_to_recommend):
        keywords_similarities = self.prepare_data(document_to_recommend.keywords)

        # Normalize similarities
        max_similarities = np.max(keywords_similarities)
        if max_similarities == 0:
            print("No matches found.")
            return {}

        normalized_similarities = (keywords_similarities * self.weight) / max_similarities

        # Map probabilities to document IDs
        probs_by_doc_dict = {doc_id: prob for doc_id, prob in zip(self.documents.get_documents().keys(), normalized_similarities)}

        return probs_by_doc_dict