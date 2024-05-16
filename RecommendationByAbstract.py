import tensorflow_hub as hub
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from RecommendationDetails import RecommendationDetails

WEIGHT = 0.3
METHOD_NAME = 'By Abstract'
class RecommendationByAbstract:
    def __init__(self):
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        self.weight = WEIGHT
        self.method_name = METHOD_NAME
        self.tfidf_vectorizer = TfidfVectorizer()

    def get_recommendations(self, article, document_to_recommend):
        abstracts = [article.get_abstract(), document_to_recommend.get_abstract()]
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(abstracts)
        top_keywords = {}

        # Calculation of cosine similarity between the two abstracts
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        doc_method_probability = similarity_scores.flatten()[0]
        top_keywords['result'] = doc_method_probability


        return RecommendationDetails(self.method_name, doc_method_probability, top_keywords, self.weight)