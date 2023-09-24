import customtkinter as ctk
from moviepy.editor import VideoFileClip
import os
from PIL import Image, ImageTk
from functionalities import resize_image


class FileChooser(ctk.CTkFrame):
    def __init__(self, parent, get_file_path):
        super().__init__(master=parent, fg_color="transparent")
        # self.grid(column=0, columnspan=2, row=0, sticky="nsew")
        self.pack(expand=True)

        self.get_file_path = get_file_path

        ctk.CTkLabel(self, text="Choose a File").pack(side="left")
        ctk.CTkButton(self, text="Browse", command=get_file_path).pack(side="left", padx=10)


class VideoDetails(ctk.CTkFrame):
    def __init__(self, parent, video_path):
        super().__init__(master=parent)
        self.pack(expand=True)

        self.video = VideoFileClip(video_path)
        self.video_info = {
            "Name": os.path.basename(self.video.filename),
            "Size": self.video.size,
            "Duration": self.video.duration
        }

        # Get a frame from the video (The first frame)
        frame = self.video.get_frame(0)
        # Save the frame as a thumbnail image using PIL
        self.image = Image.fromarray(frame)
        # resize the image to a smaller size
        self.image = resize_image(self.image)

        # Label to display the thumbnail Image
        thumbnail_img = ImageTk.PhotoImage(self.image)
        thumbnail_label = ctk.CTkLabel(self, text="", image=thumbnail_img)
        thumbnail_label.image = thumbnail_img
        thumbnail_label.pack(side="left")

        # Create a frame to hold video details
        details_frame = ctk.CTkFrame(self, fg_color="transparent")
        details_frame.pack(side="left", padx=20)

        # Create labels for video details and add them in the details frame
        for key, value in self.video_info.items():
            detail_label = ctk.CTkLabel(details_frame, text=f"{key}: {value}", font=("Arial", 16))
            detail_label.pack(anchor="w")


class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent, back_func, next_func):
        super().__init__(master=parent, fg_color="transparent")
        self.pack()

        back_button = ctk.CTkButton(self, text="BACK", command=back_func)
        back_button.pack(side="left", anchor="se", padx=50, pady=50)
        next_button = ctk.CTkButton(self, text="NEXT", command=next_func)
        next_button.pack(side="left", anchor="se", padx=50, pady=50)

