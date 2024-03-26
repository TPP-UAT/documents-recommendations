from FilesMapper import FilesMapper
from RecommendationByAbstract import RecommendationByAbstract
from RecommendationByKeywordsNumberSimilarities import RecommendationByKeywordsNumberSimilarities
from RecommendationByKeywordsCosine import RecommendationByKeywordsCosine
from RecommendationByKeywordsHierarchy import RecommendationByKeywordsHierarchy

class Recommendation:
    def __init__(self, document_to_recommend):
        self.recommendation_types = [RecommendationByKeywordsNumberSimilarities(), RecommendationByKeywordsCosine(), RecommendationByKeywordsHierarchy(), RecommendationByAbstract()]
        self.document_to_recommend = document_to_recommend

    def get_recommendation(self):
        files_mapper = FilesMapper()
        files_mapper.parse_documents()
        documents = files_mapper.get_documents()

        recommendations = []
        for recommendation_instance in self.recommendation_types:
            recommendation_instance.initialize(documents)
            recommendation = recommendation_instance.get_recommendations(self.document_to_recommend)
            recommendations.append(recommendation)

        # Combine the probabilities
        combined_probabilities = {}
        documents = files_mapper.get_documents().iter_documents()

        for doc in documents:
            doc_id = doc.get_id()
            probability = sum(recommendation.get(doc_id, 0) for recommendation in recommendations)
            combined_probabilities[doc_id] = probability

        # Check for combined probabilities
        if not combined_probabilities:
            print("No recommendations could be made for the documents provided.")
            return

        # Normalize the probabilities between 0 and 1
        max_probability = max(combined_probabilities.values())
        if max_probability == 0:
            print("All probabilities combined are zero.")
            return

        normalized_probabilities = {doc_id: probability / max_probability for doc_id, probability in combined_probabilities.items()}

        return normalized_probabilities
