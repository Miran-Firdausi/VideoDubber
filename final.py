import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from moviepy.editor import VideoFileClip, AudioFileClip

def extract_audio_from_video(video_path, audio_output_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_output_path)
        video_clip.close()
        audio_clip.close()
        print(f"Audio extracted and saved to {audio_output_path}")
    except Exception as e:
        print(f"Error: {e}")

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
    os.system(f"mpg123 {output_file}")

def merge_audio_with_video(video_path, audio_path, output_video_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        # Set the audio of the video to the translated audio
        video_clip = video_clip.set_audio(audio_clip)

        # Write the merged video to the output file
        video_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

        video_clip.close()
        audio_clip.close()
        print(f"Merged video saved as {output_video_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    input_video_path = "test.mp4"
    audio_output_path = "output_audio.wav"
    output_text_file = "output_text.txt"
    output_audio_file = "output_audio.mp3"
    target_language = "hi"
    output_merged_video_path = "output_merged_video.mp4"

    extract_audio_from_video(input_video_path, audio_output_path)

    text = convert_speech_to_text(audio_output_path)
    print("Text from audio:", text)

    translated_text = translate_text(text, target_language)
    print(f"Translated text ({target_language}):", translated_text)

    convert_text_to_audio(translated_text, output_audio_file, target_language)
    print("Translated audio saved as", output_audio_file)

    merge_audio_with_video(input_video_path, output_audio_file, output_merged_video_path)
