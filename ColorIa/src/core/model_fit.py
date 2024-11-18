import pandas as pd
from gensim.models import Word2Vec
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import EarlyStopping
# Charger le jeu de données
df = pd.read_csv('ColorIa\src\data\Augmented_French_Colors_Dataset.csv')

# Prétraitement avec Word2Vec
descriptions = df['Description de la couleur'].apply(lambda x: x.split())
model_word2vec = Word2Vec(sentences=descriptions, vector_size=200, window=10, min_count=1, workers=4)
model_word2vec.train(descriptions, total_examples=len(descriptions), epochs=30)

def get_average_word2vec(tokens_list, model, size=200):
    vec = np.zeros(size).reshape((1, size))
    count = 0
    for word in tokens_list:
        try:
            vec += model.wv[word].reshape((1, size))
            count += 1
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return vec

X = np.concatenate([get_average_word2vec(desc, model_word2vec, 200) for desc in descriptions])

# Conversion des codes hexadécimaux en RGB normalisés
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]

Y = np.array([hex_to_rgb(code) for code in df['Code Hexadécimal']])

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Création du modèle de réseau de neurones avec régularisation
model = tf.keras.Sequential([
    tf.keras.layers.Dense(512, activation='relu', input_shape=(200,)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(3, activation='sigmoid')  # Sortie pour les valeurs RGB entre 0 et 1
])

# Compiler le modèle
model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError(), metrics=['mae'])

# Callback pour arrêt anticipé si la perte de validation n'améliore pas
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Entraîner le modèle avec les ajustements
history = model.fit(
    X_train, Y_train,
    epochs=100,                   # Augmenter le nombre d'époques pour une convergence stable
    validation_split=0.2,
    batch_size=64,                # Ajustement de la taille de batch
    verbose=1,
    callbacks=[early_stopping]    # Arrêt anticipé pour éviter le surapprentissage
)

# Évaluer le modèle
Y_pred = model.predict(X_test)
mse = mean_squared_error(Y_test, Y_pred) * 255**2  # Remettre dans l'échelle RGB pour l'interprétation
print(f'Erreur quadratique moyenne : {mse}')

# Exemple de prédiction avec le modèle
test_phrases = ["bleu", "rouge", "jaune", "bleu marine", "cyan", "argent", "noir translucide", "rouge pâle", "le soleil et rouge lumineux","la mer et bleu marine","bleu sarcelle"]
for phrase in test_phrases:
    tokens = phrase.split()
    vector = get_average_word2vec(tokens, model_word2vec, 200)
    prediction_rgb = model.predict(vector).flatten() * 255  # Convertir les prédictions en valeurs RGB
    predicted_hex = "#{:02x}{:02x}{:02x}".format(int(prediction_rgb[0]), int(prediction_rgb[1]), int(prediction_rgb[2]))
    print(f'Phrase : "{phrase}" -> Couleur prédite : {predicted_hex}')

# Sauvegarder le modèle TensorFlow
model.save("color_model.h5")

# Sauvegarder le modèle Word2Vec
model_word2vec.save("word2vec_model")