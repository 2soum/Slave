from fastapi import FastAPI, File
from fastapi.responses import JSONResponse
import vosk
from Model.VoxStt import reconnaissance_vocale
import tensorflow as tf
from gensim.models import Word2Vec
import numpy as np
# Initialisation de l'application FastAPI
app = FastAPI()

# Charger le modèle Vosk une seule fois
model_address = "C:/Users/raven/Project/Slave/model/SttVoxModel/vosk-model-small-fr-0.22"
model = vosk.Model(model_address)
model_color_ia = tf.keras.models.load_model("color_model.h5", custom_objects={'MeanSquaredError': tf.keras.losses.MeanSquaredError()})
model_word2vec = Word2Vec.load("word2vec_model")
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
        texte = reconnaissance_vocale(model,audio)
        return {"output": texte.strip()}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur lors du traitement de l'audio : {str(e)}"}
        )