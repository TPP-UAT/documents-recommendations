import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationByKeywordsCosine:
    def __init__(self, documents):
        self.documents = documents
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def prepare_data(self, new_keywords):
        keywords_by_document = self.documents.get_keywords_by_document()
        print("KEYWORDS:", keywords_by_document)
        
        embeddings_keywords_by_document = []
        
        # Convertir las palabras clave en una sola cadena
        new_keywords_combined = ' '.join(new_keywords)
        embeddings_new_keywords = self.embed([new_keywords_combined])

        # Obtener representaciones vectoriales para las palabras clave de cada documento
        for document_keywords in keywords_by_document.values():
            document_keywords_combined = ' '.join(document_keywords)
            embeddings_keywords_by_document.append(self.embed([document_keywords_combined]))

        embeddings_keywords_by_document = np.array(embeddings_keywords_by_document)
        
        # Calcular la similitud del coseno entre las representaciones vectoriales de las palabras clave de los documentos y las nuevas palabras clave
        similarities = cosine_similarity(embeddings_keywords_by_document.reshape(len(embeddings_keywords_by_document), -1), embeddings_new_keywords)

        return similarities.flatten()

    def get_recommendations(self, new_keywords):
        print("Recommendations:")
        keywords_similarities = self.prepare_data(new_keywords)

        # Normalize similarities
        max_similarities = np.max(keywords_similarities)
        if max_similarities == 0:
            print("No matches found.")
            return {}

        normalized_similarities = keywords_similarities / max_similarities

        # Map probabilities to document IDs
        probs_by_doc_dict = {doc_id: prob for doc_id, prob in zip(self.documents.get_documents().keys(), normalized_similarities)}

        # Print recommendations
        for doc_id, probability in probs_by_doc_dict.items():
            print(f"Document: {doc_id}, Probability: {probability}")

        return probs_by_doc_dict