from Recommendator import Recommendator
from DocumentToRecommend import DocumentToRecommend

def print_results(recommendations):
    if not recommendations:
        print("No recommendations could be made.")
        return
    else:
        # Print the top 3 recommendations
        print("\n -----------------Top 3 recommendations:")
        for article_id, recommendation in recommendations.items():
            print(f"Article ID: {article_id}, Total Probability: {recommendation[-1]}")

if __name__ == '__main__':
    file_path = 'data/PDFs/Asphaug_2021_Planet._Sci._J._2_200.pdf'

    document_to_recommend = DocumentToRecommend(file_path)
    recommendator = Recommendator(document_to_recommend)
    recommendations = recommendator.get_recommendation()
    print_results(recommendations)

