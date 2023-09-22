import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import tkinter as tk
from tkinter import filedialog

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
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')

        video_clip.close()
        audio_clip.close()
        print(f"Merged video saved as {output_video_path}")
    except Exception as e:
        print(f"Error: {e}")

def open_file_dialog(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def process_video():
    input_video_path = input_video_entry.get()
    audio_output_path = "output_audio.wav"
    output_text_file = "output_text.txt"
    output_audio_file = "output_audio.mp3"
    target_language = target_language_entry.get()
    output_merged_video_path = "output_merged_video.mp4"

    extract_audio_from_video(input_video_path, audio_output_path)

    text = convert_speech_to_text(audio_output_path)
    output_text_entry.delete(1.0, tk.END)
    output_text_entry.insert(tk.END, "Text from audio: " + text)

    translated_text = translate_text(text, target_language)
    output_text_entry.insert(tk.END, f"\nTranslated text ({target_language}): {translated_text}")

    convert_text_to_audio(translated_text, output_audio_file, target_language)

    merge_audio_with_video(input_video_path, output_audio_file, output_merged_video_path)
    result_label.config(text="Merged video saved as " + output_merged_video_path)


root = tk.Tk()
root.title("Video Translation Tool")


input_video_label = tk.Label(root, text="Input Video:")
input_video_entry = tk.Entry(root, width=40)
input_video_button = tk.Button(root, text="Browse", command=lambda: open_file_dialog(input_video_entry))

target_language_label = tk.Label(root, text="Target Language:")
target_language_entry = tk.Entry(root, width=10)

process_button = tk.Button(root, text="Process Video", command=process_video)

output_text_entry = tk.Text(root, width=50, height=10)
result_label = tk.Label(root, text="")


input_video_label.pack()
input_video_entry.pack()
input_video_button.pack()
target_language_label.pack()
target_language_entry.pack()
process_button.pack()
output_text_entry.pack()
result_label.pack()

root.mainloop()
