import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

# Documentos relacionados con política, deporte y comida sana junto con sus frases clave
documentos = [
    {"texto": "La política fiscal es un tema clave en la economía actual.", "frases_clave": ["política económica", "medidas fiscales"]},
    {"texto": "El deporte es una forma de mantenerse saludable y activo.", "frases_clave": ["deporte saludable", "vida activa"]},
    {"texto": "Una alimentación balanceada es esencial para una vida sana y longeva.", "frases_clave": ["comida saludable", "longevidad"]},
    {"texto": "El gobierno ha anunciado nuevas medidas fiscales que afectarán a la población.", "frases_clave": ["política fiscal", "anuncio de gobierno"]},
    {"texto": "El fútbol es uno de los deportes más populares en todo el mundo.", "frases_clave": ["deporte popular", "fútbol"]},
    {"texto": "Las ensaladas y las frutas son opciones saludables para comer.", "frases_clave": ["comida saludable", "ensaladas y frutas"]},
]

# Frases clave para un nuevo documento
nuevo_documento_frases_clave = ["política argentina", "deporte extremo", "vida activa"]

# Cargar el modelo de Universal Sentence Encoder (USE) pre-entrenado
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Crear embeddings para los documentos existentes y el nuevo documento
documentos_embeddings = embed([doc["texto"] for doc in documentos])
nuevo_documento_embeddings = embed(nuevo_documento_frases_clave)

# Calcular la similitud de coseno entre el nuevo documento y todos los documentos existentes
similitudes = tf.reduce_sum(tf.multiply(documentos_embeddings, tf.expand_dims(nuevo_documento_embeddings, 1)), axis=2)

# Normalizar las similitudes para obtener probabilidades
def softmax(x):
    e_x = tf.exp(x - tf.reduce_max(x))
    return e_x / tf.reduce_sum(e_x)

probabilidades = softmax(similitudes)

# Ahora puedes ver las probabilidades para cada documento
for i, probabilidad in enumerate(probabilidades[0]):
    print(f"Probabilidad del documento {i + 1}: {probabilidad.numpy()}")

# También puedes encontrar el documento más probable (mayor probabilidad)
indice_documento_similar = tf.argmax(probabilidades[0]).numpy()
documento_recomendado = documentos[indice_documento_similar]["texto"]

print("Documento recomendado:", documento_recomendado)