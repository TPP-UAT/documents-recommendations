from Recommendation import Recommendation

def print_results(recommendations):
    if not recommendations:
        print("No recommendations could be made.")
        return

    print("Recommendations:")
    for doc_id, probability in recommendations.items():
        print(f"Documento: {doc_id}, Probabilidad: {probability}")


if __name__ == '__main__':
    new_keywords = ['Space probes', 'The Moon', 'Lunar composition', 'Lunar surface']
    text_to_recommend = "This a text from lunar surface"


    weight_cosine = 0.5
    weight_similarities = 0.2
    weight_hierarchy = 0.3
    recommendator = Recommendation(weight_cosine, weight_similarities, weight_hierarchy)
    recommendations = recommendator.get_recommendation(new_keywords)

    #print_results(recommendations)