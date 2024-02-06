import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from FilesMapper import FilesMapper
from Documents import Documents
from RecommendationByKeywords import RecommendationByKeywords
from RecommendationByAbstract import RecommendationByAbstract

def print_results(recommendations):
    print("Recommendations:")
    for doc_id, probability in recommendations.items():
        print(f"Document: {doc_id}, Probability: {probability}")

def get_recomendation_by(recommendation_instance, data_to_recommend):
    return recommendation_instance.get_recommendations(data_to_recommend)

if __name__ == '__main__':
    print('------------------------------------------\n\n')
    files_mapper = FilesMapper()
    files_mapper.parse_documents()

    documents = files_mapper.get_documents()

    new_keywords = ['Lunar probes', 'Lunar science', 'The Moon', 'Lunar composition', 'Lunar surface']
    text_to_recommend = "This a text from lunar surface"


    # Search for recommendations by keywords
    recommendations = get_recomendation_by(RecommendationByKeywords(documents), new_keywords)

    # Search for recommendations by abstract
    #recommendations = get_recomendation_by(RecommendationByAbstract(documents), text_to_recommend)

    #print_results(recommendations)
