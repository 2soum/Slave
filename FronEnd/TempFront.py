import tkinter as tk
from FronEnd.FrontHandler import lancer_reconnaissance_vocale

# Dictionnaire des couleurs et des LEDs (cercles)
couleurs_dict = {
    "rouge": "red",
    "bleu": "blue",
    "vert": "green",
    "jaune": "yellow",
    "blanc": "white",
    "noir": "black",
    "orange": "orange",
    "violet": "purple",
    "rose": "pink"
}

def illuminer_led(couleur):
    try:
        for nom_couleur, cercle in led_dict.items():
            canvas.itemconfig(cercle, outline="black", width=2)

        # Si la couleur est reconnue, illuminer la LED correspondante
        if couleur in led_dict:
            canvas.itemconfig(led_dict[couleur], outline="gold", width=5)
        else:
            print("Couleur non reconnue :", couleur)

    except Exception as e:
        print(f"Erreur lors de l'illumination de la LED : {e}")

# Interface graphique avec Tkinter
fenetre = tk.Tk()
fenetre.title("LED vocales")
fenetre.geometry("500x500")

# Créer un canevas pour afficher les LED (cercles)
canvas = tk.Canvas(fenetre, width=400, height=400)
canvas.pack(pady=20)

# Dictionnaire pour stocker les références des cercles (LED)
led_dict = {}

# Positionnement initial des cercles (LED)
positions = [
    (100, 100), (200, 100), (300, 100),
    (100, 200), (200, 200), (300, 200),
    (100, 300), (200, 300), (300, 300)
]

# Créer les cercles représentant les LED et les stocker dans le dictionnaire
for (nom_couleur, color), (x, y) in zip(couleurs_dict.items(), positions):
    cercle = canvas.create_oval(x-30, y-30, x+30, y+30, fill=color, outline="black", width=2)
    led_dict[nom_couleur] = cercle

# Ajout d'un bouton pour lancer la reconnaissance vocale
bouton = tk.Button(fenetre, text="Dites une couleur", command=lambda: lancer_reconnaissance_vocale(illuminer_led), font=("Arial", 14))
bouton.pack(pady=20)

# Lancement de la fenêtre principale
fenetre.mainloop()
