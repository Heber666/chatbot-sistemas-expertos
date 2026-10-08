"""Fragmentacion y recuperacion de documentos con TF-IDF."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def dividir_texto(texto, tamano=1000):
    palabras = texto.split()
    return [" ".join(palabras[inicio:inicio + tamano]) for inicio in range(0, len(palabras), tamano)]


def buscar_informacion_relevante(pregunta, fragmentos, cantidad=3):
    if not fragmentos:
        return []
    vectorizador = TfidfVectorizer()
    try:
        matriz = vectorizador.fit_transform(fragmentos + [pregunta])
    except ValueError:
        return []
    similitudes = cosine_similarity(matriz[-1], matriz[:-1])[0]
    indices = similitudes.argsort()[::-1][:cantidad]
    return [fragmentos[indice] for indice in indices if similitudes[indice] > 0]