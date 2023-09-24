import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os


def convert_speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error: {e}"


def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text


def convert_text_to_audio(text, output_file, language='en'):
    tts = gTTS(text=text, lang=language)
    tts.save(output_file)
    os.system(
        f"mpg123 {output_file}")


if __name__ == "__main__":
    input_audio_file = "16BFD421-DB77-4BE3-8D5E-94A35498D404.wav"
    output_text_file = "output_text.txt"
    output_audio_file = "output_audio.mp3"
    target_language = "mr"


    text = convert_speech_to_text(input_audio_file)
    print("Text from audio:", text)


    translated_text = translate_text(text, target_language)
    print(f"Translated text ({target_language}):", translated_text)


    convert_text_to_audio(translated_text, output_audio_file, target_language)
    print("Translated audio saved as", output_audio_file)
