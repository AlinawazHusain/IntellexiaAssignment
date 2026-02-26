import whisper
from deep_translator import GoogleTranslator
from torch.cuda import is_available


class WhisperTranscriber:
    '''
    Singleton Class for openai whisteper model
    '''
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            device = "cuda" if is_available() else "cpu"
            print("Loading Whisper model...")
            cls._model = whisper.load_model(name = "base" , device = device)

        return cls._instance

    def get_model(self):
        return self._model
    

    def process_audio(self, file_path, fp16 = True):
        print("Translation.....")
        result =  self._model.transcribe(file_path , fp16 = fp16)

        detected_lang = result["language"]
        text = result["text"]


        if detected_lang in ["hi", "hindi" , "ur", "urdu"]:
            translated = GoogleTranslator(source='hi', target='en').translate(text)
            return {
                "detected_language": "Hindi" if detected_lang in ["hi" , "hindi"] else "Urdu", 
                "original_text": text,
                "translated_text": translated,
                "translated_to": "English"
            }

        elif detected_lang in ["en", "english"]:
            translated = GoogleTranslator(source='en', target='hi').translate(text)
            return {
                "detected_language": "English",
                "original_text": text,
                "translated_text": translated,
                "translated_to": "Hindi"
            }

        else:
            return {
                "detected_language": detected_lang,
                "original_text": text,
                "translated_text": None,
                "translated_to": "Unsupported language"
            }