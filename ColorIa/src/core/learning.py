from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Initialiser le modèle k-NN
knn = KNeighborsRegressor(n_neighbors=3)

# Entraîner le modèle sur les données d'entraînement
knn.fit(X_train, Y_train)

# Tester le modèle sur les données de test
Y_pred = knn.predict(X_test)

# Calculer l'erreur moyenne quadratique
mse = mean_squared_error(Y_test, Y_pred)
print(f'Erreur quadratique moyenne : {mse}')

# Exemple de prédiction avec une nouvelle description de couleur
nouvelle_description = "rouge écarlate".split()
vecteur_nouvelle_description = get_average_word2vec(nouvelle_description, model_word2vec, 100)
prediction_rgb = knn.predict(vecteur_nouvelle_description)

# Affichage du résultat
print(f'Prédiction RGB pour "rouge écarlate" : {prediction_rgb}')
