import json

class KeywordsHierarchyMapper:

    # This class only serves to create the UATPretty.json, keeping the ID, name, parents and children of each keyword.

    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def map_json_to_hierarchy(self):
        # Load the JSON
        with open(self.json_file_path, 'r') as f:
            json_data = json.load(f)

        # Data structure to store the keyword hierarchy
        keywords_hierarchy = {}

        # Process the JSON to extract relevant information
        for key, value in json_data.items():
            keyword_id = key.split("/")[-1]
            pref_label = value.get("http://www.w3.org/2004/02/skos/core#prefLabel", [{}])[0].get("value", None)
            broader = self.extract_ids(value.get("http://www.w3.org/2004/02/skos/core#broader", []))
            narrower = self.extract_ids(value.get("http://www.w3.org/2004/02/skos/core#narrower", []))

            # Store the information in the data structure
            keywords_hierarchy[keyword_id] = {
                "pref_label": pref_label,
                "broader": broader,
                "narrower": narrower
            }

        return keywords_hierarchy

    def extract_ids(self, values):
        ids = []
        for v in values:
            if isinstance(v, dict) and "value" in v:
                ids.append(v["value"].split("/")[-1])
            elif isinstance(v, str):
                ids.append(v.split("/")[-1])
        return ids

    def save_hierarchy_as_json(self, output_file_path):
        # Map the keyword hierarchy
        keywords_hierarchy = self.map_json_to_hierarchy()

        # Save the hierarchy as JSON
        with open(output_file_path, 'w') as f:
            json.dump(keywords_hierarchy, f, indent=4)

# Example usage of the script
if __name__ == "__main__":
    input_json_path = "UAT.json"  # Path of the input JSON file
    output_json_path = "UATPretty.json"  # Path of the output JSON file

    mapper = KeywordsHierarchyMapper(input_json_path)
    mapper.save_hierarchy_as_json(output_json_path)
