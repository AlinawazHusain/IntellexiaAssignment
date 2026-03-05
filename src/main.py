import whisper_service
import text_to_speech_service 
import translation_service


import warnings
warnings.filterwarnings("ignore")


stt_model = whisper_service.WhisperTranscriber()
translation_model = translation_service.Translator()
tts_model = text_to_speech_service.TextToSpeech()




if __name__ == "__main__":


    file_path = "../input_files/example1.mp3"
    output_path = "../output_files/example1.mp3"


    try:
        # result = stt_model.process_audio(file_path)
        result = {'detected_language': 'hi', 'original_text': ' यहां मूल पाथ का एक सरल और मज़ेदार सारांश हिंदी में दिया घया है। आज से साट साल पहले जंगल इतने घने थे और जानवर इतने सारे कि पूचो मत। तब शिकार करना एक जबर्दस्त फैशन था। जिसकी दिवार पर शेर या तेंदूए का सिर नहीं होता था, उसे समाज में कमतर ही माना जाता था। बड़े-बड़े अफसर और शरीफ आदमी शेर मारने जाते थे। और कुछ तो अपनी सरकारी डेटी से चोरी चिपे गायब रहकर जूठे नाम से शिकार के मज़ेडार किस्से भी लिखते थे। ताकि किसी को पता ना चले कि वो कितनी चुट्टिया मार रहे हैं। लेकिन हर कोई बंदूक लेकर नहीं गोमता था। जानवरों को गोली नहीं उनकी शानडार फोटो खीजते थे। आज जब लेकः ने एक पूराने महावत से पूचा तो उस बूजूर्ग ने बताएए कि जहां वो बचपन में चामपियं साहब के साथ शेर देखा करते थे, वहाँ अब एक भी शेर नहीं मिलता। अफसोस, उन्निसो पचास के दशक में ढेर सारे शिकार के चकर में भिचारे सारे शेर ऐसे गायब हुए कि अब उनके पोस्टर भी ढोणने से नहीं मिलते। शायद तब लोगों ने सोचा होगा इतने सारे शेर हैं, थोड़ा और मार लेते हैं। और अब पचताय होत क्या जब चिडिया चुख गई कहेत।', 'translated_to': 'en'}
        print(result)
        translated_text = translation_model.translate_text(result["original_text"], result["detected_language"] , result["translated_to"])
        print(translated_text)
        # translate_into = 'hi' if 
        tts_model.convert_text_to_speech(translated_text , output_path , result["translated_to"])

    except Exception as e:
        print(str(e))