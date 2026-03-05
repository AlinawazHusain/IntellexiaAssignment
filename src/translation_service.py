# import torch
# import re
# from transformers import AutoTokenizer, AutoModelForCausalLM


# class LLMTranslator:

#     _instance = None

#     MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

#     MAX_INPUT_TOKENS = 3500
#     CONTEXT_SENTENCES = 3


#     def __new__(cls):

#         if cls._instance is None:

#             cls._instance = super().__new__(cls)

#             print("Loading LLM translator...")

#             cls.tokenizer = AutoTokenizer.from_pretrained(cls.MODEL_NAME)

#             cls.model = AutoModelForCausalLM.from_pretrained(
#                 cls.MODEL_NAME,
#                 torch_dtype=torch.float16,
#                 device_map="auto"
#             )

#         return cls._instance


#     # -----------------------
#     # Sentence splitter
#     # -----------------------

#     def split_sentences(self, text):

#         sentences = re.split(r'(?<=[.!?।])\s+', text)

#         return [s.strip() for s in sentences if s.strip()]


#     # -----------------------
#     # Chunk builder
#     # -----------------------

#     def build_chunks(self, sentences):

#         chunks = []
#         current = ""

#         for s in sentences:

#             candidate = current + " " + s

#             tokens = len(self.tokenizer.encode(candidate))

#             if tokens > self.MAX_INPUT_TOKENS:

#                 chunks.append(current.strip())

#                 current = s

#             else:

#                 current = candidate

#         if current:
#             chunks.append(current.strip())

#         return chunks


#     # -----------------------
#     # Prompt builder
#     # -----------------------

#     def build_prompt(self, text, src, tgt):

#         lang_map = {
#             "hi": "Hindi",
#             "en": "English"
#         }

#         src_lang = lang_map[src]
#         tgt_lang = lang_map[tgt]

#         prompt = f"""
# You are a professional translator.

# Translate the following text from {src_lang} to {tgt_lang}.

# Rules:
# - Preserve meaning and context
# - Do NOT summarize
# - Keep narrative tone
# - Produce natural {tgt_lang}

# Text:
# {text}

# Translation:
# """

#         return prompt


#     # -----------------------
#     # LLM inference
#     # -----------------------

#     def translate_chunk(self, text, src, tgt):

#         prompt = self.build_prompt(text, src, tgt)

#         inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

#         output = self.model.generate(
#             **inputs,
#             max_new_tokens=1200,
#             temperature=0.2,
#             top_p=0.9
#         )

#         result = self.tokenizer.decode(output[0], skip_special_tokens=True)

#         return result.split("Translation:")[-1].strip()


#     # -----------------------
#     # Main translation
#     # -----------------------

#     def translate_text(self, text, src="hi", tgt="en"):

#         if src not in ["hi", "en"] or tgt not in ["hi", "en"]:
#             raise ValueError("Supported languages: hi, en")

#         sentences = self.split_sentences(text)

#         chunks = self.build_chunks(sentences)

#         translated_chunks = []

#         context_buffer = []

#         for chunk in chunks:

#             context = " ".join(context_buffer[-self.CONTEXT_SENTENCES:])

#             combined = context + "\n\n" + chunk

#             translated = self.translate_chunk(combined, src, tgt)

#             translated_chunks.append(translated)

#             context_buffer.append(chunk)

#         return "\n\n".join(translated_chunks)



import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

# -----------------------------
# Translator
# -----------------------------
class Translator:
    _instance = None
    _model_map = {
        "hi2en": "Helsinki-NLP/opus-mt-hi-en",
        "en2hi": "Helsinki-NLP/opus-mt-en-hi",
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._models = {}
            for key, model_name in cls._model_map.items():
                print(f"Loading model {model_name}...")
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                cls._models[key] = {"tokenizer": tokenizer, "model": model}
        return cls._instance

    def translate_text(self, text, src, tgt):
        key = f"{src}2{tgt}"
        if key not in self._models:
            raise ValueError(f"No model for {src} → {tgt}")

        tokenizer = self._models[key]["tokenizer"]
        model = self._models[key]["model"]

        # Split into sentences to preserve context
        sentences = re.split(r'(?<=[.!?]) +', text)
        translated_sentences = []

        for sentence in sentences:
            encoded = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                generated_tokens = model.generate(**encoded, max_length=512)
            translated = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            translated_sentences.append(translated)

        return " ".join(translated_sentences)

