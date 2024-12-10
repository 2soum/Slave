import io
import json
import wave
import logging
from vosk import KaldiRecognizer
import soundfile as sf
from scipy.signal import resample
from fastapi.responses import JSONResponse

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reconnaissance_vocale(model, audio):
    """
    Traite un chunk audio (en bytes) et effectue la reconnaissance vocale.

    Args:
        model: Modèle Kaldi pour la reconnaissance vocale.
        audio (bytes): Données audio en bytes.

    Returns:
        str: Texte reconnu.
    """
    try:
        # Si un objet BytesIO est passé, convertissez-le en bytes
        if isinstance(audio, io.BytesIO):
            audio = audio.getvalue()
        logger.info("Début du traitement audio.")
        audio_stream = io.BytesIO(audio)
        wf = wave.open(audio_stream, "rb")

        # Vérification du format audio
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            wf.close()
            logger.error("Format audio invalide. Requis: mono WAV 16kHz avec 16 bits.")
            return JSONResponse(
                status_code=400,
                content={"error": "Le fichier audio doit être mono WAV 16kHz avec une profondeur de 16 bits"}
            )

        # Initialisation du modèle de reconnaissance vocale
        recognizer = KaldiRecognizer(model, wf.getframerate())
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            recognizer.AcceptWaveform(data)

        # Extraction du résultat final
        final_result = json.loads(recognizer.FinalResult())
        logger.info(f"Résultat brut de la reconnaissance vocale : {final_result}")

        # Récupération du texte reconnu
        texte = final_result.get("text", "")
        if not isinstance(texte, str):
            wf.close()
            logger.error("Le champ 'text' dans le résultat n'est pas une chaîne valide.")
            return JSONResponse(
                status_code=500,
                content={"error": "Le champ 'text' dans le résultat n'est pas une chaîne valide"}
            )

        wf.close()
        logger.info(f"Texte reconnu avec succès : {texte}")
        return texte.strip()

    except Exception as e:
        logger.error(f"Erreur interne : {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur interne : {str(e)}"}
        )


def audio_processing(audio_bytes):
    """
    Convertit un fichier audio en bytes en un format accepté par `reconnaissance_vocale`.

    Args:
        audio_bytes (bytes): Données audio brutes.

    Returns:
        io.BytesIO: Fichier audio converti au format mono, WAV 16kHz.

    Raises:
        ValueError: Si une erreur survient lors de la conversion.
    """
    try:
        # Charger l'audio à partir des bytes
        audio_io = io.BytesIO(audio_bytes)
        data, original_sample_rate = sf.read(audio_io)

        # Vérifier que l'audio a été correctement chargé
        if data is None or len(data) == 0:
            raise ValueError("Le fichier audio est vide ou invalide.")

        # Si l'audio est stéréo, convertir en mono
        if len(data.shape) > 1:  # Plusieurs canaux présents
            data = data.mean(axis=1)  # Moyenne des canaux pour obtenir le mono

        # Conversion de la fréquence d'échantillonnage à 16kHz
        target_sample_rate = 16000
        num_samples = round(len(data) * target_sample_rate / original_sample_rate)
        resampled_data = resample(data, num_samples)

        # Sauvegarder les données converties au format WAV dans un flux binaire
        output_io = io.BytesIO()
        sf.write(output_io, resampled_data, target_sample_rate, format='wav')
        
        # Repositionner le pointeur du flux au début
        output_io.seek(0)

        return output_io
    except ValueError as ve:
        raise ValueError(f"Erreur lors du traitement audio : {ve}")
    except Exception as e:
        raise ValueError(f"Erreur inattendue lors du traitement audio : {str(e)}")