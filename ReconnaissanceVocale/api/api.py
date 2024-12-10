from fastapi import FastAPI, File
import vosk
from Model.VoxStt import reconnaissance_vocale, audio_processing
from fastapi.responses import JSONResponse

# Initialisation de l'application FastAPI
app = FastAPI()

# Charger le modèle Vosk une seule fois
model_address = "../../SttVoxModel/vosk-model-small-fr-0.22"
model = vosk.Model(model_address)

@app.post("/recognize-bytes")
async def recognize_audio_bytes(audio: bytes = File(...)):
    """
    Endpoint pour reconnaître la parole à partir de bytes audio.

    Args:
        audio (bytes): Données audio en bytes.

    Returns:
        JSON: Texte reconnu.
    """
    try:
        # Reconnaissance vocale
        texte = reconnaissance_vocale(model, audio_processing(audio))

        # Si `reconnaissance_vocale` retourne un JSONResponse (en cas d'erreur), il faut le transmettre.
        if isinstance(texte, JSONResponse):
            return texte

        # Retour du texte reconnu dans le format simplifié
        return {"output": texte}

    except Exception as e:
        return {"error": f"Erreur lors du traitement de l'audio : {str(e)}"}
