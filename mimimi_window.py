import sys
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import pygame

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GIF_PATH = os.path.join(SCRIPT_DIR, "d890b6445597de2f0c1b69f0f9573e91.gif")
SOUND_PATH = os.path.join(SCRIPT_DIR, "mimimi-clash-royale.mp3")


class MimimiWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("МИ-МИ-МИ!")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_PATH)

        self.gif_image = Image.open(GIF_PATH)
        self.frames = []
        self.frame_durations = []

        for frame in ImageSequence.Iterator(self.gif_image):
            frame_rgba = frame.convert("RGBA")
            self.frames.append(ImageTk.PhotoImage(frame_rgba.copy()))
            duration = frame.info.get("duration", 100)
            self.frame_durations.append(duration)

        self.frame_index = 0
        self.label = tk.Label(self.root)
        self.label.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.play_sound()
        self.animate()

    def play_sound(self):
        pygame.mixer.music.play()

    def animate(self):
        if not self.frames:
            return
        self.label.configure(image=self.frames[self.frame_index])
        delay = self.frame_durations[self.frame_index]
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(delay, self.animate)

    def on_close(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MimimiWindow()
    app.run()
