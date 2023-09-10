import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from FilesMapper import FilesMapper
from RecommendationByKeywords import RecommendationByKeywords
from RecommendationByAbstract import RecommendationByAbstract

if __name__ == '__main__':
    print('------------------------------------------\n\n')
    files_mapper = FilesMapper()
    files_mapper.parse_documents()

    documents = files_mapper.get_documents()

    new_keywords = ['Lunar surface', 'Lunar science', 'Lunar impacts']

    # Search for recommendations by keywords
    # recommendation_by_keywords = RecommendationByKeywords(documents)
    # recommendations = recommendation_by_keywords.get_recommendations(new_keywords)
    # print("Recommendations: ", recommendations)

    new_text = "This a text from lunar surface"

    # Search for recommendations by abstract
    recommendation_by_keywords = RecommendationByAbstract(documents)
    recommendations = recommendation_by_keywords.get_recommendations(new_text)
    print("Recommendations: ", recommendations)