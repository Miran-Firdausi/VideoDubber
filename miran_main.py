import sys
from moviepy.editor import *
import speech_recognition as sr
import pyttsx3

# Extract audio from Video
video = VideoFileClip(sys.argv[1])
audio = video.audio
audio.write_audiofile(sys.argv[2], codec='pcm_s16le')

# Text to Speech
# Initialize the recognizer
r = sr.Recognizer()


# Function to convert text to
# speech
def speak_text(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


# Loop infinitely for user to
# speak

while True:
    # Exception handling to handle
    # exceptions at the runtime
    try:
        # audio_file = sys.argv[2]

        # use the microphone as source for input.
        with sr.AudioFile("audio.wav") as source:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            # r.adjust_for_ambient_noise(source)

            # listens for the user's input
            audio_data = r.record(source)

            # Using google to recognize audio
            MyText = r.recognize_google(audio_data)
            MyText = MyText.lower()

            print("Did you say ", MyText)
            speak_text(MyText)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")
