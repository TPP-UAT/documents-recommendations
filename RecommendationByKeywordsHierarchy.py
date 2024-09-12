import json
from RecommendationDetails import RecommendationDetails

METHOD_NAME = 'Keywords Hierarchy'
WEIGHT = 0.2

class RecommendationByKeywordsHierarchy:
    def __init__(self):
        self.json_file_path = "UATPretty.json"
        self.weight = WEIGHT
        self.method_name = METHOD_NAME


    def build_hierarchy(self):
        with open(self.json_file_path, 'r') as f:
            json_data = json.load(f)

        # Build hierarchy from JSON data
        hierarchy = {}
        for keyword_id, keyword_info in json_data.items():
            broader = [broader_id.split("/")[-1] for broader_id in keyword_info.get("broader", [])]
            narrower = [narrower_id.split("/")[-1] for narrower_id in keyword_info.get("narrower", [])]
            hierarchy[keyword_id] = {
                "pref_label": keyword_info.get("pref_label"),
                "broader": broader,
                "narrower": narrower
            }
        return hierarchy
    
    def find_keyword_id_by_value(self, target_value, hierarchy):
        for key, value in hierarchy.items():
            if value["pref_label"] == target_value:
                return key
        return None

    def calculate_probability_for_keyword(self, article_keyword, keywords_to_recommend, hierarchy):
        probability = 0.0
        if article_keyword in keywords_to_recommend:
            # If the keyword matches one of the new keywords, set probability to 1
            probability = 1.0
        else:
            # Check if the keyword or any of its ancestors are in the new keywords
            keyword_id = self.find_keyword_id_by_value(article_keyword, hierarchy)
            if keyword_id:
                ancestors = self.get_ancestors(keyword_id, hierarchy)
                for ancestor, depth in ancestors.items():
                    if hierarchy[ancestor]["pref_label"] in keywords_to_recommend:
                        # Adjust probability based on hierarchy depth
                        if depth == 1:
                            probability += 0.5
                        elif depth == 2:
                            probability += 0.25
        return probability

    def get_ancestors(self, keyword_id, hierarchy):
        ancestors = {}
        queue = [(keyword_id, 0)]  # Store depth along with keyword_id
        while queue:
            current_keyword_id, depth = queue.pop(0)
            broader_keywords_ids = hierarchy[current_keyword_id]["broader"]
            for broader_id in broader_keywords_ids:
                ancestors[broader_id] = depth + 1
                queue.append((broader_id, depth + 1))
        return ancestors
        
    def get_recommendations(self, article, document_to_recommend):
        keywords_to_recommend = document_to_recommend.get_keywords()
        article_keywords = article.get_keywords()
        hierarchy = self.build_hierarchy()

        doc_method_probability = 0
        top_keywords = {}
        max_keyword_probability = 0

        for article_keyword in article_keywords:
            keyword_probability = self.calculate_probability_for_keyword(article_keyword, keywords_to_recommend, hierarchy)
            doc_method_probability += keyword_probability
            if keyword_probability > max_keyword_probability:
                top_keywords[article_keyword] = keyword_probability

        return RecommendationDetails(self.method_name, doc_method_probability, top_keywords, self.weight)
