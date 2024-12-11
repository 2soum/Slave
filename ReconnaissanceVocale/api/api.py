from fastapi import FastAPI, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import vosk
from Model.VoxStt import reconnaissance_vocale, audio_processing
from fastapi.responses import JSONResponse
from color import couleur_to_hex
import tensorflow as tf
from gensim.models import Word2Vec
import io
from pydub import AudioSegment
import tempfile

# Initialisation de l'application FastAPI
app = FastAPI()

# Configuration de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le modèle Vosk une seule fois
try:
    model_address = "../../SttVoxModel/vosk-model-small-fr-0.22"
    model = vosk.Model(model_address)
except Exception as e:
    raise RuntimeError(f"Échec de l'initialisation du modèle Vosk : {e}")

try:
    model_coloria = tf.keras.models.load_model(
        "../../color_model.h5", custom_objects={'MeanSquaredError': tf.keras.losses.MeanSquaredError()}
    )
    model_word2vec = Word2Vec.load("../../word2vec_model")
except Exception as e:
    raise RuntimeError(f"Échec de l'initialisation du modèle colorIa : {e}")

def convert_to_wav(audio_bytes: bytes, input_format: str) -> bytes:
    """
    Convertit les données audio en format WAV si nécessaire.
    
    Args:
        audio_bytes (bytes): Les données audio brutes
        input_format (str): Le format d'entrée (ex: 'webm', 'mp3')
        
    Returns:
        bytes: Les données audio au format WAV
    """
    try:
        # Créer un fichier temporaire pour l'audio d'entrée
        with tempfile.NamedTemporaryFile(suffix=f'.{input_format}', delete=False) as temp_in:
            temp_in.write(audio_bytes)
            temp_in_path = temp_in.name

        # Charger l'audio avec pydub
        audio = AudioSegment.from_file(temp_in_path, format=input_format)
        
        # Configurer le format WAV approprié pour Vosk
        audio = audio.set_frame_rate(16000)  # Vosk attend 16kHz
        audio = audio.set_channels(1)        # Mono
        audio = audio.set_sample_width(2)    # 16-bit
        
        # Convertir en WAV et retourner les bytes
        wav_io = io.BytesIO()
        audio.export(wav_io, format='wav')
        return wav_io.getvalue()
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur lors de la conversion audio : {str(e)}"
        )

def detect_audio_format(audio_bytes: bytes) -> str:
    """
    Détecte le format audio à partir des premiers octets.
    
    Args:
        audio_bytes (bytes): Les données audio brutes
        
    Returns:
        str: Le format détecté ('wav', 'webm', etc.)
    """
    # Signatures des formats audio courants
    signatures = {
        b'RIFF': 'wav',
        b'\x1a\x45\xdf\xa3': 'webm',
        b'ID3': 'mp3',
        b'\xff\xfb': 'mp3',
        b'OggS': 'ogg'
    }
    
    # Vérifier les premiers octets pour détecter le format
    for signature, format_name in signatures.items():
        if audio_bytes.startswith(signature):
            return format_name
            
    return 'unknown'

@app.post("/recognize-bytes")
async def recognize_audio_bytes(audio: bytes = File(...)):
    """
    Endpoint pour reconnaître la parole à partir de bytes audio.
    Convertit automatiquement en WAV si nécessaire.

    Args:
        audio (bytes): Données audio en bytes.

    Returns:
        JSON: Texte reconnu ou code hexadécimal correspondant.
    """
    try:
        # Détecter le format audio
        audio_format = detect_audio_format(audio)
        
        # Convertir en WAV si ce n'est pas déjà le cas
        if audio_format != 'wav':
            print(f"Converting from {audio_format} to WAV")
            audio = convert_to_wav(audio, audio_format)
        
        # Traitement et reconnaissance vocale
        texte = reconnaissance_vocale(model, audio_processing(audio))

        # Vérification si une erreur a été retournée
        if isinstance(texte, JSONResponse):
            return texte

        # Conversion du texte en code hexadécimal
        couleur = couleur_to_hex(texte.lower(), model_word2vec, model_coloria)
        if not couleur:
            raise HTTPException(status_code=404, detail="Couleur non reconnue dans la base de données.")

        return {"output": couleur}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        return {"error": f"Erreur lors du traitement de l'audio : {str(e)}"}