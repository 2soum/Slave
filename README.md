
# LED Vocales avec Reconnaissance Vocale

Ce projet permet de contrôler l'illumination de LED virtuelles (représentées par des cercles sur une interface Tkinter) en disant simplement le nom d'une couleur via la reconnaissance vocale.

## Prérequis

### Systèmes d'exploitation

Ce projet fonctionne sur **Windows** et **Linux**. Les étapes d'installation sont différentes pour chaque système d'exploitation.

### Python

Assurez-vous d'avoir **Python 3.6** ou une version supérieure d'installée sur votre machine.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-projet.git
cd votre-projet
```

### 2. Créer un environnement virtuel (optionnel mais recommandé)

```bash
python -m venv env
source env/bin/activate   # Sur Linux ou macOS
env\Scripts\activate    # Sur Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Installer les dépendances système

#### Sur Windows

Pour Windows, vous devez installer **PyAudio** en utilisant une roue binaire (wheel), car l'installation via `pip` peut échouer. Téléchargez le fichier approprié depuis [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

Ensuite, installez-le avec `pip` :

```bash
pip install chemin/vers/le/fichier_wheel.whl
```

#### Sur Linux

Sur Linux, installez `portaudio` avant de continuer avec `PyAudio` :

```bash
sudo apt-get install portaudio19-dev
```

Ensuite, installez `PyAudio` normalement :

```bash
pip install pyaudio
```

### 5. Exécuter l'application

Lancez le script principal pour démarrer l'application :

```bash
python main.py
```

## Fonctionnement

1. Cliquez sur le bouton "Dites une couleur".
2. Dites une couleur parmi les suivantes : rouge, bleu, vert, jaune, blanc, noir, orange, violet, rose.
3. La LED correspondante (cercle) sur l'interface sera illuminée.

## Dépendances

- `speech_recognition` : Pour la reconnaissance vocale.
- `pyaudio` : Pour capturer l'audio via le microphone.
- `tkinter` : Pour l'interface graphique.
