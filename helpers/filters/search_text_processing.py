
import re
import unicodedata
from html import unescape

import nltk
from nltk.corpus import stopwords

# Download stopwords if not available
nltk.download("stopwords")
STOPWORDS_ES = set(stopwords.words("spanish"))

def clean_text(text):
    """Cleans text by removing HTML, URLs, special characters, and normalizing spaces."""
    if not text:
        return ""

    text = remove_html(text)
    # text = unicodedata.normalize('NFD', text) # Eliminar acentos y diacríticos
    # text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # Eliminar caracteres especiales, mantener solo letras, números y espacios
    text = re.sub(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>?/¡¿]', '', text) # Elimina símbolos
    text = re.sub(r'\s+', ' ', text).strip() # Normalizar espacios (eliminar múltiples spaces y strip)
    text = text.lower()

    tokens = text.split()
    tokens = [word for word in tokens if word not in STOPWORDS_ES]
    return " ".join(tokens)

def remove_html(text):
    text = unescape(text) # Decodificar entidades HTML
    text = re.sub(r'<[^>]+>', '', text) # Eliminar etiquetas HTML
    return text