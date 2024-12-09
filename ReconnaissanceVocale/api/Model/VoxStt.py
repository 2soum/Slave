import json
import io
import wave
from starlette.responses import JSONResponse
from vosk import KaldiRecognizer



def reconnaissance_vocale(model, audio):
    """
    Traite un chunk audio (en bytes) et effectue la reconnaissance vocale.

    Args:
        audio (bytes): Données audio en bytes.

    Returns:
        str: Le texte reconnu, ou une chaîne vide si aucune reconnaissance complète.
    """
    audio_stream = io.BytesIO(audio)
    wf = wave.open(audio_stream, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        return JSONResponse(
            status_code=400,
            content={"error": "Le fichier audio doit être mono WAV 16kHz avec une profondeur de 16 bits"}
        )
    recognizer = KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        recognizer.AcceptWaveform(data)
    final_result = json.loads(recognizer.FinalResult())
    texte = final_result.get("text", "")
    wf.close()

    return texte.strip()

