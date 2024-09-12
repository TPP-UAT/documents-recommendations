import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity
from RecommendationDetails import RecommendationDetails

WEIGHT = 0.2
METHOD_NAME = 'Keywords Cosine'
MIN_PROBABILITY = 0.7
class RecommendationByKeywordsCosine:
    def __init__(self):
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        self.documents = None
        self.weight = WEIGHT
        self.method_name = METHOD_NAME


    def get_recommendations(self, article, document_to_recommend):
        keywords_to_recommend = document_to_recommend.get_keywords()
        article_keywords = article.get_keywords()

        total_doc_probability = 0
        top_keywords = {}
        
        for keyword_to_recommend in keywords_to_recommend:
            embeddings_new_keyword = self.embed([keyword_to_recommend])
            for article_keyword in article_keywords:
                embeddings_doc_keyword = self.embed([article_keyword])
                similarity = cosine_similarity(embeddings_new_keyword, embeddings_doc_keyword)[0][0]
                total_doc_probability += similarity
                if similarity > MIN_PROBABILITY:
                    top_keywords[article_keyword] = similarity

        return RecommendationDetails(self.method_name, total_doc_probability, top_keywords, self.weight)
            