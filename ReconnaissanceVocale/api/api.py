from fastapi import FastAPI, File, HTTPException
import vosk
from Model.VoxStt import reconnaissance_vocale, audio_processing
from fastapi.responses import JSONResponse
from color import couleur_to_hex
import tensorflow as tf
from gensim.models import Word2Vec

# Initialisation de l'application FastAPI
app = FastAPI()
# Charger le modèle Vosk une seule fois
try:
    model_address = "../../SttVoxModel/vosk-model-small-fr-0.22"
    model = vosk.Model(model_address)
except Exception as e:
    raise RuntimeError(f"Échec de l'initialisation du modèle Vosk : {e}")
try:
    model_coloria = tf.keras.models.load_model("../../color_model.h5", custom_objects={'MeanSquaredError': tf.keras.losses.MeanSquaredError()})
    model_word2vec = Word2Vec.load("../../word2vec_model")
except Exception as e:
    raise RuntimeError(f"Échec de l'initialisation du modèle colorIa : {e}")
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
        # Traitement et reconnaissance vocale
        texte = reconnaissance_vocale(model, audio_processing(audio))

        # Vérification si une erreur a été retournée
        if isinstance(texte, JSONResponse):
            return texte

        # Conversion du texte en code hexadécimal (si correspondance trouvée)
        couleur = couleur_to_hex(texte.lower(),model_word2vec,model_coloria)
        if not couleur:
            raise HTTPException(status_code=404, detail="Couleur non reconnue dans la base de données.")

        return {"output": couleur}

    except HTTPException as http_ex:
        # Gérer les exceptions FastAPI
        raise http_ex
    except Exception as e:
        # Gérer toute autre erreur
        return {"error": f"Erreur lors du traitement de l'audio : {str(e)}"}
