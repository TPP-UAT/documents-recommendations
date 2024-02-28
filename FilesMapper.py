import fitz
import os
import re
from Document import Document
from Documents import Documents

DOCUMENTS_PATH = 'data/test/'

class FilesMapper:
    def __init__(self):
        self.documents = Documents()
        self.files_path = DOCUMENTS_PATH
    
    # Getters
    def get_documents(self):
        return self.documents
    
    def parse_keywords(self, text):
        regex = r'Uniﬁed Astronomy Thesaurus concepts:\s*((?:[^;)]+\(\d+\);\s*)+[^;)]+\(\d+\))'

        urls = re.findall(regex, text)
        
        if len(urls) > 0:
            parts = urls[0].split(';')

            # Iterar a través de las partes y extraer el texto deseado
            result = [part.split('(')[0].strip().replace('\n', ' ') for part in parts]
            return result
    
    def parse_abstract(self, text):
        regex_pattern = r'Abstract([\s\S]*?)Uniﬁed Astronomy Thesaurus concepts:'
        extracted_text = ''
        match = re.search(regex_pattern, text[0])

        if match:
            extracted_text += match.group(1) 

        return extracted_text
    
    def get_full_text(self, file):
        pdf_document = fitz.open(self.files_path + file)
        full_text = []
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            text = page.get_text()
            # Obtain full text from document
            full_text.append(text)
        return full_text

    def parse_documents(self):
        # Get the list of files
        files = os.listdir(DOCUMENTS_PATH)
        for file in files:
            try:
                # Obtain full text from document
                full_text = self.get_full_text(file)
                # Obtain abstract text from document
                abstract_text = self.parse_abstract([full_text[0]])
                # Obtain keywords from document
                keywords = self.parse_keywords(full_text[0])

                document = Document(file, abstract_text, keywords, full_text)
                self.documents.add_document(document)
            except:
                print("Error trying to load file with path: ", file)