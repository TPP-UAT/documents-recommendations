class RecommendationDetails:
    def __init__(self, method_name, doc_method_probability, top_keywords, weight):
        self.recommendation_method = method_name
        self.doc_method_probability = doc_method_probability
        self.top_keywords = top_keywords
        self.weight = weight

    #Getters
    def get_recommendation_name_method(self):
        return self.recommendation_method

    def get_weight(self):
        return self.weight
        
    def get_doc_probability(self):
        return self.doc_method_probability
    
    def get_top_keywords(self):
        return self.top_keywords