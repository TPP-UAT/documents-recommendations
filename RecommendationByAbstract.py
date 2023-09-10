import tensorflow as tf
import tensorflow_hub as hub

class RecommendationByAbstract:
    def __init__(self, documents):
        self.documents = documents

    def prepare_data(self, new_text):
        abstract_by_document = self.documents.get_abstracts()
        print("NEW TEXT: ", new_text)
        # Load the pre-trained Universal Sentence Encoder (USE) model
        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

        # Create embeddings for the existing documents and the new document
        abstracts_embeddings = embed(abstract_by_document)
        new_abstracts_embeddings = embed([new_text])[0]

        return abstracts_embeddings, new_abstracts_embeddings
    
    def softmax(self, x):
        e_x = tf.exp(x - tf.reduce_max(x))
        return e_x / tf.reduce_sum(e_x)

    def get_recommendations(self, new_text):
        # Prepare the data for processing
        abstracts_embeddings, new_abstracts_embeddings = self.prepare_data(new_text)

        # Calculate the cosine similarity between the new document and the existing documents
        similarities = tf.reduce_sum(tf.multiply(abstracts_embeddings, tf.expand_dims(new_abstracts_embeddings, 0)), axis=1)
        probabilities = self.softmax(similarities)

        print("probabilities: ", probabilities)
        probs_by_doc = {}
        document_probability_index = 0
        for _, doc in self.documents.get_documents().items():
            probs_by_doc[doc.get_id()] = probabilities[document_probability_index]
            document_probability_index += 1
            
        return probs_by_doc
