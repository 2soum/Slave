import tensorflow as tf
from gensim.models import Word2Vec
import numpy as np

# Charger le modèle de réseau de neurones et le modèle Word2Vec
model = tf.keras.models.load_model("color_model.h5", custom_objects={'MeanSquaredError': tf.keras.losses.MeanSquaredError()})
model_word2vec = Word2Vec.load("word2vec_model")

# Fonction de transformation Word2Vec pour obtenir le vecteur moyen d'une description de couleur
def get_average_word2vec(description, model, size=200):
    tokens = description.split()
    vec = np.zeros(size).reshape((1, size))
    count = 0
    for word in tokens:
        try:
            vec += model.wv[word].reshape((1, size))
            count += 1
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return vec

# Fonction principale pour obtenir le code hexadécimal
def couleur_to_hex(description):
    vector = get_average_word2vec(description, model_word2vec, 200)
    prediction_rgb = model.predict(vector).flatten() * 255  # Convertir la sortie en RGB
    predicted_hex = "#{:02x}{:02x}{:02x}".format(
        int(prediction_rgb[0]), int(prediction_rgb[1]), int(prediction_rgb[2])
    )
    return predicted_hex

# Utilisation simple
couleur = "cyan"
codehexa = couleur_to_hex(couleur)
print(f"Couleur '{couleur}' -> Code hexadécimal prédit : {codehexa}")
