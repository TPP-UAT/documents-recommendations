from RecommendationDetails import RecommendationDetails

WEIGHT = 0.2
METHOD_NAME = 'Number of Similarity'

class RecommendationByKeywordsNumberSimilarities:
    def __init__(self):
        self.embed = None
        self.weight = WEIGHT
        self.method_name = METHOD_NAME
  

    def get_recommendations(self, article, document_to_recommend):
        keywords_to_recommend = document_to_recommend.get_keywords()
        article_keywords = article.get_keywords()
        count_common_keywords = 0
        top_keywords = {}
        for article_keyword in article_keywords:
            if article_keyword in keywords_to_recommend:
                count_common_keywords += 1
                top_keywords[article_keyword] = 1/len(article_keywords)

        doc_method_probability = count_common_keywords/(len(article_keywords))

        return RecommendationDetails(self.method_name, doc_method_probability, top_keywords, self.weight)
