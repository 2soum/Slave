import vosk
import json
import io
import wave
from slave.model.ColorIa.core import couleur_to_hex
from starlette.responses import JSONResponse



def reconnaissance_vocale(model,audio):
    """
    Traite un chunk audio (en bytes) et effectue la reconnaissance vocale.

    Args:
        audio_bytes (bytes): Données audio en bytes.

    Returns:
        str: Le texte reconnu, ou une chaîne vide si aucune reconnaissance complète.
    """
    audio_stream = io.BytesIO(audio)
    wf = wave.open(audio_stream, "rb")

    # Vérifier les caractéristiques du fichier audio
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        return JSONResponse(
            status_code=400,
            content={"error": "Le fichier audio doit être mono WAV 16kHz avec une profondeur de 16 bits"}
        )

    # Initialiser le recognizer avec vosk (réutilise l'instance de modèle)
    recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

    # Lecture des frames audio et reconnaissance vocale
    texte = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            texte += result.get("text", "") + " "

    # Fermer le fichier wave
    wf.close()
    return texte

def generation_rgb(description ,model, model_word2vec):
    hexa = couleur_to_hex(description,model,model_word2vec)
    return hexa