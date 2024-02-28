import json
from FilesMapper import FilesMapper
from Documents import Documents
from RecommendationByAbstract import RecommendationByAbstract
from RecommendationByKeywordsNumberSimilarities import RecommendationByKeywordsNumberSimilarities
from RecommendationByKeywordsCosine import RecommendationByKeywordsCosine
from RecommendationByKeywordsHierarchy import RecommendationByKeywordsHierarchy

class Recommendation:
    def __init__(self, weight_cosine, weight_similarities, weight_hierarchy):
        self.weight_cosine = weight_cosine
        self.weight_similarities = weight_similarities
        self.weight_hierarchy = weight_hierarchy

    def get_recommendation_by(self, recommendation_instance, data_to_recommend):
        return recommendation_instance.get_recommendations(data_to_recommend)

    def get_recommendation(self, data_to_make_recommendation):
        files_mapper = FilesMapper()
        files_mapper.parse_documents()
        documents = files_mapper.get_documents()

        # Get recommendations by number of keyword similarities
        recommendations_by_similarities = self.get_recommendation_by(RecommendationByKeywordsNumberSimilarities(documents), data_to_make_recommendation)

        # Get recommendations by keyword cosine similarity
        recommendations_by_cosine = self.get_recommendation_by(RecommendationByKeywordsCosine(documents), data_to_make_recommendation)

        # Get recommendations by keyword hierarchy
        recommendations_by_hierarchy = self.get_recommendation_by(RecommendationByKeywordsHierarchy(documents, "UATPretty.json"), data_to_make_recommendation)

        # Get recommendations by Abstract
        #recommendations_by_abstract = self.get_recommendation_by(RecommendationByAbstract(documents), 'This is a text from a Earth-moon system')

        # Combine the probabilities with the weights
        combined_probabilities = {}
        documents = files_mapper.get_documents().iter_documents()

        for doc in documents:
            doc_id = doc.get_id()
            probability = (
                recommendations_by_similarities.get(doc_id, 0) * self.weight_similarities +
                recommendations_by_cosine.get(doc_id, 0) * self.weight_cosine +
                recommendations_by_hierarchy.get(doc_id, 0) * self.weight_hierarchy
            )
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
