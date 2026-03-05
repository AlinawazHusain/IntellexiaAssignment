import whisper

class WhisperTranscriber:
    '''
    Singleton Class for openai whisteper model
    '''
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            print("Loading Whisper model...")
            cls._model = whisper.load_model(name = "medium")

        return cls._instance

    def get_model(self):
        return self._model
    

    def process_audio(self, file_path, fp16 = True):
        print("Transcribing.....")
        result =  self._model.transcribe(file_path , fp16 = fp16)

        detected_lang = result["language"]
        text = result["text"]

        print(detected_lang)


        if detected_lang in ["hi", "hindi"]:
            return {
                "detected_language": "hi", 
                "original_text": text,
                "translated_to": "en"
            }
        
        elif detected_lang in ["ur", "urdu"]:
            return {
                "detected_language": "ur", 
                "original_text": text,
                "translated_to": "en"
            }
        

        elif detected_lang in ["en", "english"]:
            return {
                "detected_language": "en",
                "original_text": text,
                "translated_to": "hi"
            }

        else:
            return {
                "detected_language": detected_lang,
                "original_text": text,
                "translated_to": "Unsupported language"
            }