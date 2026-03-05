from TTS.api import TTS
from gtts import gTTS

class TextToSpeech:
    _instance = None
    _tts_en = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("Loading English TTS model...")
            cls._tts_en = TTS(model_name="tts_models/en/ljspeech/vits")
        return cls._instance

    def convert_text_to_speech(self, text, output_path, language="en"):
        if language == "en":
            print("Converting English text to speech...")
            self._tts_en.tts_to_file(text=text, file_path=output_path)
        elif language == "hi":
            print("Converting Hindi text to speech using gTTS...")
            tts_hi = gTTS(text=text, lang="hi")
            tts_hi.save(output_path)
        else:
            raise ValueError(f"Language '{language}' not supported")

        print("Done")