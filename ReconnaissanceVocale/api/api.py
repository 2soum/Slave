from fastapi import FastAPI, File
import vosk
from Model.VoxStt import reconnaissance_vocale, audio_processing
from fastapi.responses import JSONResponse

# Initialisation de l'application FastAPI
app = FastAPI()

# Charger le modèle Vosk une seule fois
model_address = "../../SttVoxModel/vosk-model-small-fr-0.22"
model = vosk.Model(model_address)

# Dictionnaire pour mapper les mots clés à leurs codes hexadécimaux (incluant les teintes foncées)
color_map = {
    "rouge": "#FF0000",
    "rouge bordeaux": "#800000",
    "vert": "#00FF00",
    "vert foncé": "#006400",
    "bleu": "#0000FF",
    "bleu marine": "#000080",
    # Ajoutez d'autres couleurs et nuances ici
}

@app.post("/recognize-bytes")
async def recognize_audio_bytes(audio: bytes = File(...)):
    """
    Endpoint pour reconnaître la parole à partir de bytes audio.

    Args:
        audio (bytes): Données audio en bytes.

    Returns:
        JSON: Texte reconnu ou code hexadécimal correspondant.
    """
    try:
        # Reconnaissance vocale
        texte = reconnaissance_vocale(model, audio_processing(audio))

        # Si `reconnaissance_vocale` retourne un JSONResponse (en cas d'erreur), il faut le transmettre.
        if isinstance(texte, JSONResponse):
            return texte
        # Vérification si le texte correspond à une couleur dans le dictionnaire
        couleur = texte.lower()
        if couleur in color_map:
            return {"output": color_map[couleur]}

        # Retour du texte reconnu dans le format simplifié si aucune correspondance n'est trouvée
        return {"output": texte}
    except Exception as e:
        return {"error": f"Erreur lors du traitement de l'audio : {str(e)}"}
