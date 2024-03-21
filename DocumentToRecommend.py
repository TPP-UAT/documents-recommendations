import fitz
import re

class DocumentToRecommend:
    def __init__(self, file_path):
        self.file_path = file_path
        self.keywords = self.get_keywords()
        self.abstract = self.get_abstract()

    # Retrieve the full text from an article
    def get_full_text_from_file(self):
        pdf_document = fitz.open(self.file_path)
        full_text = []
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            text = page.get_text()
            full_text.append(text)
        
        pdf_document.close()
        return full_text[0]

    def get_keywords(self):
        keywords = []
        target_text = "Uniﬁed Astronomy Thesaurus concepts:"
        full_text = self.get_full_text_from_file()
            
        # Buscar el texto objetivo en la página actual
        if target_text in full_text:
            # Extraer las palabras clave del texto objetivo
            start_index = full_text.index(target_text)
            end_index = start_index + len(target_text)
            target_text_snippet = full_text[end_index:]
            # Buscar las palabras clave separadas por punto y coma
            for line in target_text_snippet.split('\n'):
                line = line.strip()
                if not line:
                    break
                # Verificar si hay punto y coma en la línea
                if ';' in line:
                    keywords.extend(line.split(';'))
                else:
                    break  # Si no hay punto y coma, terminar de buscar palabras clave
    
        keywords_with_ids = [keyword.strip() for keyword in keywords if keyword.strip()]
        keywords = [re.sub(r'\s*\(\d+\)', '', keyword) for keyword in keywords_with_ids]
        return keywords
    
    def get_abstract(self):
        full_text = self.get_full_text_from_file()
        regex_pattern = r'Abstract([\s\S]*?)Uniﬁed Astronomy Thesaurus concepts:'
        extracted_abstract = ''
        match = re.search(regex_pattern, full_text)

        if match:
            extracted_abstract += match.group(1)
        return extracted_abstract