from Recommendation import Recommendation
import fitz
import re

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
    document_to_recommend = 'data/PDFs/Asphaug_2021_Planet._Sci._J._2_200.pdf'
    target_text = "Uniﬁed Astronomy Thesaurus concepts:"
    keywords = []

    # Extraer las palabras clave del texto del documento PDF
    document = fitz.open(document_to_recommend)
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text()
        
        # Buscar el texto objetivo en la página actual
        if target_text in text:
            # Extraer las palabras clave del texto objetivo
            start_index = text.index(target_text)
            end_index = start_index + len(target_text)
            target_text_snippet = text[end_index:]
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
            break  # Terminar la búsqueda después de encontrar el texto objetivo
    
    keywords_with_ids = [keyword.strip() for keyword in keywords if keyword.strip()]
    keywords = [re.sub(r'\s*\(\d+\)', '', keyword) for keyword in keywords_with_ids]

    # Aquí puedes usar las palabras clave encontradas para hacer recomendaciones utilizando tu clase Recommendation
    weight_cosine = 0.5
    weight_similarities = 0.2
    weight_hierarchy = 0.3
    recommendator = Recommendation(document_to_recommend, keywords, weight_cosine, weight_similarities, weight_hierarchy)
    recommendations = recommendator.get_recommendation(keywords)
    print_results(recommendations)
