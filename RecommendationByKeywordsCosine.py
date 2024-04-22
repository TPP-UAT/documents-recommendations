import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationByKeywordsCosine:
    def __init__(self):
        self.embed = None
        self.documents = None

    def initialize(self, documents):
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        self.documents = documents

    def prepare_data(self, new_keywords):
        if self.documents is None:
            raise ValueError("Documents have not been initialized. Call initialize() first.")

        keywords_by_document = self.documents.get_keywords_by_document()
        detailed_similarity_scores = {}

        for doc_id, document_keywords in keywords_by_document.items():
            detailed_similarity_scores[doc_id] = {"total_similarity": 0, "top_keyword": "", "top_similarity": 0}
            for keyword in new_keywords:
                embeddings_new_keyword = self.embed([keyword])
                for doc_keyword in document_keywords:
                    embeddings_doc_keyword = self.embed([doc_keyword])
                    similarity = cosine_similarity(embeddings_new_keyword, embeddings_doc_keyword)[0][0]
                    detailed_similarity_scores[doc_id]["total_similarity"] += similarity
                    if similarity > detailed_similarity_scores[doc_id]["top_similarity"]:
                        detailed_similarity_scores[doc_id]["top_similarity"] = similarity
                        detailed_similarity_scores[doc_id]["top_keyword"] = doc_keyword

        max_total_similarity = max(score["total_similarity"] for score in detailed_similarity_scores.values())
        for doc_id, scores in detailed_similarity_scores.items():
            normalized_total_similarity = (scores["total_similarity"] / max_total_similarity) if max_total_similarity > 0 else 0
            scores["total_similarity"] = normalized_total_similarity

        return detailed_similarity_scores

    def get_recommendations(self, document_to_recommend):
        if self.documents is None:
            raise ValueError("Documents have not been initialized. Call initialize() first.")

        keywords_similarities = self.prepare_data(document_to_recommend.keywords)
        return {
            doc_id: {
                "probability": details["total_similarity"],
                "top_keyword": details["top_keyword"],
                "top_similarity": details["top_similarity"]
            } for doc_id, details in keywords_similarities.items()
        }
