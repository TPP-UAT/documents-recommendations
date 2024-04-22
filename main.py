from Recommendation import Recommendation
from DocumentToRecommend import DocumentToRecommend

def print_results(recommendations):
    if not recommendations:
        print("No recommendations could be made.")
        return

    print("Recommendations:")
    for doc_id, probability in recommendations.items():
        print(f"Documento: {doc_id}, Probabilidad: {probability}")

if __name__ == '__main__':
    file_path = 'data/PDFs/Asphaug_2021_Planet._Sci._J._2_200.pdf'

    document_to_recommend = DocumentToRecommend(file_path)
    recommendator = Recommendation(document_to_recommend)
    recommendations = recommendator.get_recommendation()
    print_results(recommendations)
