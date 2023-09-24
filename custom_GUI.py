import customtkinter as ctk
from file_chooser import *
from main_screen import *
from functionalities import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry("1100x700+0+0")
        self.title("Video Dubber")
        self.minsize(1100, 700)

        # Shared variables
        self.video_path = None

        # Layout configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=6)

        # Widget
        self.heading = ctk.CTkLabel(self, text="Video Dubber", font=("Ebrima Bold", 32))
        self.heading.place(relx=0.5, y=50, anchor="center")
        self.file_chooser_frame = FileChooser(self, self.get_file_path)
        # self.translation_frame = TextTranslation(self)
        self.video_details_frame = None
        self.buttons_frame = None
        self.translation_frame = None

        # run
        self.mainloop()

    # Functions
    def get_file_path(self):
        self.video_path = choose_video_file()
        self.file_chooser_frame.pack_forget()
        self.video_details_frame = VideoDetails(self, self.video_path)
        self.buttons_frame = ButtonsFrame(self, self.go_back, self.go_next)

    def go_back(self):
        self.video_details_frame.pack_forget()
        self.buttons_frame.pack_forget()
        self.file_chooser_frame.pack(expand=True)

    def go_next(self):
        self.video_details_frame.pack_forget()
        self.buttons_frame.pack_forget()
        self.heading.place_forget()
        self.translation_frame = TextTranslation(self, self.video_path)
        # VideoPreview(self, self.video_path)


App()
