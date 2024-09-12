from FilesMapper import FilesMapper
from RecommendationByKeywordsCosine import RecommendationByKeywordsCosine
from RecommendationByKeywordsNumberSimilarities import RecommendationByKeywordsNumberSimilarities
from RecommendationByKeywordsHierarchy import RecommendationByKeywordsHierarchy
from RecommendationByAbstract import RecommendationByAbstract

class Recommendator:
    def __init__(self, document_to_recommend):
        self.recommendation_types = [
            RecommendationByKeywordsCosine(),
            RecommendationByKeywordsNumberSimilarities(),
            RecommendationByKeywordsHierarchy(),
            RecommendationByAbstract()
        ]
        self.document_to_recommend = document_to_recommend

        files_mapper = FilesMapper()
        files_mapper.parse_documents()
        self.articles = files_mapper.get_documents()

            
    def get_top_3_recommendations(self, recommendation_probabilities):
        top_3_articles = [(None, float('-inf')), (None, float('-inf')), (None, float('-inf'))]

        for article_id, article_recommendation in recommendation_probabilities.items():
            article_probability = article_recommendation[-1]
            if article_probability > top_3_articles[0][1]:
                top_3_articles[2] = top_3_articles[1]
                top_3_articles[1] = top_3_articles[0]
                top_3_articles[0] = (article_id, article_probability)
            elif article_probability > top_3_articles[1][1]:
                top_3_articles[2] = top_3_articles[1]
                top_3_articles[1] = (article_id, article_probability)
            elif article_probability > top_3_articles[2][1]:
                top_3_articles[2] = (article_id, article_probability)

        top_3_recommendations = {article_id: recommendation_probabilities[article_id] for article_id, _ in top_3_articles if article_id is not None}
        return top_3_recommendations


    def get_recommendation(self):
        recommendation_probabilities = {}
        for article in self.articles.iter_documents():
            recommendation_probabilities[article.get_id()] = []

            total_probability = 0

            for recommendation_type in self.recommendation_types: 
                doc_recommendation = recommendation_type.get_recommendations(article, self.document_to_recommend)
                recommendation_probabilities[article.get_id()].append(doc_recommendation)

                weight = doc_recommendation.get_weight()
                doc_probability = doc_recommendation.get_doc_probability()

                total_probability += weight * doc_probability

            #LAST value in this arry will be the article total probability
            recommendation_probabilities[article.get_id()].append(total_probability)

        return self.get_top_3_recommendations(recommendation_probabilities)