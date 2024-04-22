from FilesMapper import FilesMapper
from RecommendationByKeywordsCosine import RecommendationByKeywordsCosine

class Recommendation:
    def __init__(self, document_to_recommend):
        # Aquí solo incluimos el método de coseno en la lista de tipos de recomendación
        self.recommendation_types = [
            ('Cosine Similarity', RecommendationByKeywordsCosine())
        ]
        self.document_to_recommend = document_to_recommend
        self.documents = None

    def load_documents(self):
        files_mapper = FilesMapper()
        files_mapper.parse_documents()
        self.documents = files_mapper.get_documents()

    def get_recommendation(self):
        if self.documents is None:
            self.load_documents()

        recommendations = []
        for name, recommendation_instance in self.recommendation_types:
            recommendation_instance.initialize(self.documents)
            recommendation = recommendation_instance.get_recommendations(self.document_to_recommend)
            recommendations.append((name, recommendation))

        combined_probabilities = {}
        best_source_by_doc = {}

        for doc in self.documents.iter_documents():
            doc_id = doc.get_id()
            combined_prob = 0.0
            best_prob = -1.0
            best_source = ""
            for name, recommendation in recommendations:
                if isinstance(recommendation, dict):  # Ensure recommendation is a dictionary
                    prob = recommendation.get(doc_id, {"probability": 0}).get("probability", 0)
                    if isinstance(prob, float):  # Check if prob is a float
                        combined_prob += prob
                        # Check to not use Abstract Similarity for explanation
                        if prob > best_prob and name != "Abstract Similarity":
                            best_prob = prob
                            best_source = name
            combined_probabilities[doc_id] = combined_prob
            if best_source:
                best_source_by_doc[doc_id] = best_source
            else:
                best_source_by_doc[doc_id] = "No other source was significant"

        if not combined_probabilities:
            print("No recommendations could be made for the documents provided.")
            return {}

        max_probability = max(combined_probabilities.values())
        if max_probability == 0:
            print("All probabilities combined are zero.")
            return {}

        normalized_probabilities = {}
        for doc_id, probability in combined_probabilities.items():
            normalized_prob = probability / max_probability
            explanation = f"Best match due to {best_source_by_doc[doc_id]}."
            normalized_probabilities[doc_id] = (normalized_prob, explanation)

        return normalized_probabilities
