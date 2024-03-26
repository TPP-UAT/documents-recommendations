import json

WEIGHT = 0.2

class RecommendationByKeywordsHierarchy:
    def initialize(self, documents):
        self.json_file_path = "UATPretty.json"
        self.documents = documents
        self.weight = WEIGHT

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

    def calculate_recommendation_probabilities(self, new_keywords):
        hierarchy = self.build_hierarchy()

        # Initialize probabilities for each document
        document_probabilities = {doc_id: 0.0 for doc_id in self.documents.get_documents().keys()}

        # Calculate probabilities based on keyword hierarchy
        for doc_id, doc_keywords in self.documents.get_keywords_by_document().items():
            for keyword in doc_keywords:
                probability = self.calculate_probability_for_keyword(keyword, new_keywords, hierarchy)
                document_probabilities[doc_id] += probability

        return document_probabilities
    
    def find_keyword_id_by_value(self, target_value):
        for key, value in self.build_hierarchy().items():
            if value["pref_label"] == target_value:
                return key
        return None

    def calculate_probability_for_keyword(self, keyword, new_keywords, hierarchy):
        probability = 0.0
        if keyword in new_keywords:
            # If the keyword matches one of the new keywords, set probability to 1
            probability = 1.0
        else:
            # Check if the keyword or any of its ancestors are in the new keywords
            keyword_id = self.find_keyword_id_by_value(keyword)
            if keyword_id:
                ancestors = self.get_ancestors(keyword_id, hierarchy)
                for ancestor, depth in ancestors.items():
                    if hierarchy[ancestor]["pref_label"] in new_keywords:
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
        
    def get_recommendations(self, document_to_recommend):
        document_probabilities = self.calculate_recommendation_probabilities(document_to_recommend.keywords)

        # Check if there are no documents, return an empty dictionary if so
        if not document_probabilities:
            return {}

        # Find the maximum probability among all documents
        max_probability = max(document_probabilities.values())

        # Check if max_probability is zero to avoid division by zero
        if max_probability == 0:
            return {}  # Return an empty dictionary if all probabilities are zero

        # Normalize probabilities
        normalized_probabilities = {doc_id: (probability * self.weight) / max_probability for doc_id, probability in document_probabilities.items()}

        recommendations = {}
        for doc_id, probability in normalized_probabilities.items():
            recommendations[doc_id] = probability

        return recommendations
