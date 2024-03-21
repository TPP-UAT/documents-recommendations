import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationByAbstract:
    def initialize(self, documents):
        self.documents = documents
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        self.weight = 0.3

    def prepare_data(self, new_abstract):
        abstracts = list(self.documents.get_abstracts_by_document().values())
        abstracts.append(new_abstract)

        # Vectorización de los abstracts
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(abstracts)

        # Cálculo de similitud coseno entre los abstracts
        similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

        return similarity_scores.flatten()

    def get_recommendations(self, document):
        similarity_scores = self.prepare_data(document.abstract)

        # Normalize similarities
        max_similarities = np.max(similarity_scores)
        if max_similarities == 0:
            print("No matches found.")
            return {}

        normalized_similarities = (similarity_scores * self.weight) / max_similarities

        # Map probabilities to document IDs and print
        probs_by_doc_dict = {doc_title: prob for doc_title, prob in zip(self.documents.get_abstracts_by_document().keys(), normalized_similarities)}
        for doc_title, prob in probs_by_doc_dict.items():
            print(f"Abstract Probability for {doc_title}: {prob}")

        return probs_by_doc_dict
