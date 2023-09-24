import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from tkinter import PhotoImage
from moviepy.editor import VideoFileClip
from functionalities import *
import subprocess
from variables import language_codes


class TextTranslation(ctk.CTkFrame):
    def __init__(self, parent, video_path):
        super().__init__(master=parent)
        self.grid(row=0, column=1, sticky="nsew")

        # Shared Variables
        self.video_path = video_path
        self.text_to_translate = None
        self.to_language = None

        # Layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=11)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # self.language_chooser_frame = ctk.CTkFrame(self).grid(row=0, column=0, sticky="ew")
        self.from_language_chooser = ctk.CTkComboBox(self, values=list(language_codes.keys()))
        self.from_language_chooser.grid(row=0, column=0, padx=5, pady=5)

        self.to_language_chooser = ctk.CTkComboBox(self, values=list(language_codes.keys()))
        self.to_language_chooser.grid(row=0, column=1, padx=5, pady=5)

        self.recognized_textbox = ctk.CTkTextbox(self, font=("arial", 22), wrap=tk.WORD)
        self.recognized_textbox.grid(row=1, column=0, sticky="nsew", padx=5)
        self.translated_textbox = ctk.CTkTextbox(self, font=("arial", 22), wrap=tk.WORD)
        self.translated_textbox.grid(row=1, column=1, sticky="nsew", padx=5)

        self.translate_button = ctk.CTkButton(self, text="Translate", command=self.translate)
        self.translate_button.grid(row=2, column=0)
        self.convert_button = ctk.CTkButton(self, text="Convert", command=self.convert)
        self.convert_button.grid(row=2, column=1)

        audio_path = extract_audio(self.video_path)
        recognized_text = recognize_speech(audio_path)
        self.recognized_textbox.insert("0.0", recognized_text)
        self.translated_text = None
        self.translate()

    def translate(self):
        self.to_language = language_codes[self.to_language_chooser.get()]
        self.text_to_translate = self.recognized_textbox.get("0.0", "end")
        self.translated_text = translate_text(self.text_to_translate, target_language=self.to_language)
        self.translated_textbox.delete("0.0", "end")
        self.translated_textbox.insert("0.0", self.translated_text)

    def convert(self):
        audio_path = text_to_audio(self.translated_text, self.to_language)
        combine_audio_with_video(self.video_path, audio_path)
        messagebox.showinfo("Video Dubber", "Video Saved Successfully.")

        video_path = "video_with_audio.mp4"
        # Use any video player to open the video
        subprocess.Popen(["start", video_path], shell=True)


# class VideoPreview(ctk.CTkCanvas):
    # def __init__(self, master, video_path):
    #     super().__init__(master, width=320, height=240)
    #     self.grid(row=0, column=0)
    #     print(video_path)
    #
    #     # Load the video
    #     self.video = VideoFileClip(video_path)
    #
    #     # Get the first frame as an image
    #     self.video_frame = self.video.get_frame(0)
    #
    #     # Convert the image to a PhotoImage (compatible with tkinter)
    #     self.photo = PhotoImage(data=self.video_frame.tobytes())
    #
    #     # Create an image item on the canvas
    #     self.image_item = self.create_image(0, 0, anchor="nw", image=self.photo)
    #
    #     # Update the video preview periodically
    #     self.update_video_preview()

    # def update_video_preview(self):
    #     # Get the next frame of the video
    #     self.video_frame = self.video.get_frame(self.video.duration / 2)  # Change the time as needed
    #
    #     # Convert the frame to a PhotoImage
    #     self.photo = PhotoImage(data=self.video_frame.tobytes())
    #
    #     # Update the image on the canvas
    #     self.itemconfig(self.image_item, image=self.photo)
    #
    #     # Schedule the next update
    #     self.after(100, self.update_video_preview)  # Adjust the update interval as needed

