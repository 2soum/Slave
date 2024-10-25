# Recognizer.py
import vosk
import pyaudio
import json

model_address = "../SttVoxModel/vosk-model-small-fr-0.22" #chargement du petit model si vous voulez le gros model Go telecharger ici https://alphacephei.com/vosk/models
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()
model = vosk.Model(model_address)
# Initialisation de PyAudio
recognizer = vosk.KaldiRecognizer(model, 16000)

def reconnaissance_vocale(callback):
    try:
        print("Dites une couleur...")
        stream.start_stream()
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                texte = json.loads(result)["text"]
                print("Vous avez dit : " + texte)

                # Appeler le callback pour illuminer la couleur détectée
                callback(texte.lower())
                stream.stop_stream()
                break  # Sortir de la boucle après la reconnaissance

    except Exception as e:
        print(f"Erreur lors de la reconnaissance vocale : {e}")
