from fastapi import FastAPI, File
from fastapi.responses import JSONResponse
import vosk
from Model.VoxStt import reconnaissance_vocale,audio_processing

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
        # Charger les bytes dans un fichier WAV en mémoire

        texte = reconnaissance_vocale(model,audio_processing(audio))
        return {"output": texte.strip()}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur lors du traitement de l'audio : {str(e)}"}
        )