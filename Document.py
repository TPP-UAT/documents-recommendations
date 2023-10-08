class Document:
    def __init__(self, id, abstract, keywords, full_text):
        self.id = id
        self.abstract = abstract
        self.keywords = keywords
        self.full_text = full_text

    # Getters
    def get_id(self):
        return self.id

    def get_abstract(self):
        return self.abstract

    def get_keywords(self):
        return self.keywords

    def get_full_text(self):
        return self.full_text
