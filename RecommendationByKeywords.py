import tensorflow as tf
import tensorflow_hub as hub

class RecommendationByKeywords:
    def __init__(self, documents):
        self.documents = documents

    def prepare_data(self, new_keywords):
        print("SIZE: ", self.documents.get_size())
        keywords_by_document = self.documents.get_keywords()
        # Load the pre-trained Universal Sentence Encoder (USE) model
        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

        # Create embeddings for the existing documents and the new document
        keywords_embeddings = embed(keywords_by_document)
        new_keywords_embeddings = embed(new_keywords)

        return keywords_embeddings, new_keywords_embeddings
    
    def softmax(self, x):
        e_x = tf.exp(x - tf.reduce_max(x))
        return e_x / tf.reduce_sum(e_x)

    def get_recommendations(self, new_keywords):
        # Prepare the data for processing
        keywords_embeddings, new_keywords_embeddings = self.prepare_data(new_keywords)

        # Calculate the cosine similarity between the new document and the existing documents
        similarities = tf.matmul(keywords_embeddings, tf.transpose(new_keywords_embeddings))
        probabilities = self.softmax(similarities)

        print("probabilities: ", probabilities)
        probs_by_doc = {}
        document_probability_index = 0
        for _, doc in self.documents.get_documents().items():
            prob_by_document = 0
            probs_by_doc[doc.get_id()] = 0
            for _ in doc.get_keywords():
                prob_by_document += sum(probabilities[document_probability_index])
                document_probability_index += 1
            probs_by_doc[doc.get_id()] = prob_by_document
            
        return probs_by_doc
