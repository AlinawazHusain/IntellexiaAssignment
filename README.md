# 🎙 Live Audio Translator

A **Python-based voice translator** that allows you to:  

- Record your voice or upload an audio file  
- Automatically transcribe it using **OpenAI Whisper**  
- Detect the language (Hindi, Urdu, English)  
- Translate it to the target language  
- Speak the translated text using TTS  

This project supports **real-time transcription**, file uploads, and playback.  

---

## **Features**

- Record audio directly from your microphone  
- Upload existing audio files
- Automatic language detection  
- Translation between Hindi, Urdu, and English  
- Plays translated text using **gTTS** (Windows) or `mpg123` (Linux/macOS)  
- Uses **Whisper** model as a singleton for efficiency  

---

## **Whisper Model Recommendation**


base -> accuracy = Medium | speed =  Fast | Good general-purpose, multi-language support 
medium -> accuracy =  High | speed = Slower | Better accuracy, recommended if speed is less critical 
large -> accuracy = Very High | speed = Slowest | Best accuracy, recommended for production if your system has enough RAM/GPU (~8 GB) |

> ⚠️ **Tip:** For best results with Hindi and Urdu transcription, use the **large** model.

---

## **Setup Instructions**

1. **Make the setup script executable** (Linux/macOS):

```bash
chmod +x setup.sh
```

2. **Run Setup Script to create virtual environment ,install all requirements and setups**

```bash
./setup.sh
```

3. **Run Setup Script to create virtual environment ,install all requirements and setups**

Linux
```bash
source venv/bin/activate
```

Windows
```bash
venv\Scripts\activate
```


4. **Run Programme**
```bash
python main.py
# or
python3 main.py
```