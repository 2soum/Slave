import pandas as pd
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Charger le jeu de données (je reprends l'exemple avec les couleurs)
df = pd.read_csv("../data/jeu_de_donnees_1million_couleurs_retry.csv")

# Diviser les descriptions de couleur en mots
descriptions = df['Description de la couleur'].apply(lambda x: x.split())

# Initialiser et entraîner le modèle Word2Vec
model_word2vec = Word2Vec(sentences=descriptions, vector_size=100, window=5, min_count=1, workers=4)
model_word2vec.train(descriptions, total_examples=len(descriptions), epochs=10)

# Conversion des descriptions en vecteurs
def get_average_word2vec(tokens_list, model, size):
    """
    Cette fonction moyenne les vecteurs Word2Vec de chaque mot pour créer un vecteur moyen par description.
    """
    vec = np.zeros(size).reshape((1, size))
    count = 0
    for word in tokens_list:
        try:
            vec += model[word].reshape((1, size))
            count += 1
        except KeyError:  # Si un mot n'est pas dans le vocabulaire de Word2Vec
            continue
    if count != 0:
        vec /= count
    return vec

# Transformer les descriptions en vecteurs Word2Vec moyens
X = np.concatenate([get_average_word2vec(desc, model_word2vec, 100) for desc in descriptions])

# Utiliser les codes couleurs RGB comme output
def hex_to_rgb(hex_color):
    """Convertit un code hexadécimal en valeurs RGB"""
    hex_color = hex_color.lstrip('#')
    return list(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Conversion des codes hexadécimaux en RGB
Y = np.array([hex_to_rgb(code) for code in df['Code Hexadécimal']])

# Séparer les données en ensemble d'entraînement et de test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
