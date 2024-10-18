import speech_recognition as sr
import tkinter as tk

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

# Fonction pour illuminer (mettre en surbrillance) la LED correspondant à la couleur dite
def illuminer_led(couleur):
    try:
        # Réinitialiser toutes les LED à leur état normal
        for nom_couleur, cercle in led_dict.items():
            canvas.itemconfig(cercle, outline="black", width=2)

        # Si la couleur est reconnue, illuminer la LED correspondante
        if couleur in led_dict:
            canvas.itemconfig(led_dict[couleur], outline="gold", width=5)
        else:
            print("Couleur non reconnue :", couleur)

    except Exception as e:
        print(f"Erreur lors de l'illumination de la LED : {e}")

# Fonction pour démarrer la reconnaissance vocale
def reconnaissance_vocale():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Ajustement au bruit ambiant... veuillez patienter...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Dites une couleur...")

        try:
            # Capture de l'audio
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            texte = recognizer.recognize_google(audio, language="fr-FR")
            print("Vous avez dit : " + texte)

            # Illuminer la LED correspondante
            illuminer_led(texte.lower())

        except sr.WaitTimeoutError:
            print("Temps écoulé, aucun son détecté.")

        except sr.UnknownValueError:
            print("Désolé, je n'ai pas compris ce que vous avez dit.")

        except sr.RequestError as e:
            print("Erreur de requête à l'API Google; {0}".format(e))

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
bouton = tk.Button(fenetre, text="Dites une couleur", command=reconnaissance_vocale, font=("Arial", 14))
bouton.pack(pady=20)

# Lancement de la fenêtre principale
fenetre.mainloop()
