import whisper_service
import tempfile
from gtts import gTTS
import os
import sounddevice as sd
from scipy.io.wavfile import write

import warnings
warnings.filterwarnings("ignore")


model = whisper_service.WhisperTranscriber()


def speak_text(text, lang):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        if os.name == "nt": 
            os.system(f'start /min {fp.name}')
        else: 
            os.system(f'mpg123 "{fp.name}"')



def record_audio(filename="recording.wav", duration=10, sample_rate=44100):
    print("🎙 Recording started...")
    audio_data = sd.rec(int(duration * sample_rate),
                        samplerate=sample_rate,
                        channels=1,
                        dtype='int16')
    sd.wait()
    print("Recording finished.")
    write(filename, sample_rate, audio_data)
    return filename 


if __name__ == "__main__":

    decision = int(input("Enter 1 for providing audio file , 2 to speak :"))
    file_path = ""
    if decision == 1:
        file_path = input("Enter audio File Path : ")
    
    elif decision == 2:
        audio_len = int(input("Enter lenght of audio you want to speak in seconds : "))
        file_path = record_audio(duration = audio_len)

    else:
        print("Unknown input , only valid inputs are 1 and 2")
        exit(0)


    try:
        result = model.process_audio(file_path)
    except Exception as e:
        print(str(e))

    if result["translated_to"] == "Hindi":
        speak_text(result["translated_text"], lang="hi")
    else:
        speak_text(result["translated_text"], lang="en")

