class Documents:
    def __init__(self):
        self.documents = {}

    # Getters
    def get_documents(self):
        return self.documents
    
    def get_by_id(self, id):
        return self.documents.get(id, None)

    def get_size(self):
        return len(self.documents)
    
    def get_keywords(self):
        keywords = []
        for _, document in self.documents.items():
            keywords.extend(document.get_keywords())
        return keywords
    
    def get_keywords_by_document(self):
        keywords_by_document = {}
        for document_id, document in self.documents.items():
            keywords_by_document[document_id] = document.get_keywords()
        return keywords_by_document
    
    def get_abstracts(self):
        abstracts = []
        for _, document in self.documents.items():
            abstracts.append(document.get_abstract())

        return abstracts
    
    def get_full_texts(self):
        full_texts = []
        for _, document in self.documents.items():
            full_texts.append(document.get_full_text())

        return full_texts
    
    def add_document(self, document):
        print("Adding document: ",document.id, document.get_keywords())
        self.documents[document.get_id()] = document
    