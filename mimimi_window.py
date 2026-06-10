import sys
import os
import argparse
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import pygame

from triggers import TRIGGERS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(SCRIPT_DIR, "sounds")
GIF_PATH = os.path.join(SCRIPT_DIR, "d890b6445597de2f0c1b69f0f9573e91.gif")
DEFAULT_SOUND = os.path.join(SCRIPT_DIR, "mimimi-clash-royale.mp3")

HAS_GIF_REACTIONS = {"mimimi"}


def _parse_args():
    parser = argparse.ArgumentParser(description="Mi-Mi-Mi Reaction Window")
    parser.add_argument("--reaction", default="mimimi")
    parser.add_argument("--text", default="")
    return parser.parse_args()


class ReactionWindow:
    def __init__(self, reaction: str, text: str):
        self.reaction_key = reaction
        self.data = TRIGGERS.get(reaction, TRIGGERS["mimimi"])
        self.user_text = text

        self.root = tk.Tk()
        self.root.title(self.data["label"])
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)

        if reaction in HAS_GIF_REACTIONS:
            self._setup_gif_mode()
        else:
            self._setup_text_mode()

        self._play_sound()
        self.root.after(2800, self._start_fadeout)
        self.root.bind("<Escape>", lambda e: self._close())
        self.root.bind("<Button-1>", lambda e: self._close())

    def _setup_gif_mode(self):
        w, h = 320, 320
        x = random.randint(50, self.root.winfo_screenwidth() - w - 50)
        y = random.randint(50, self.root.winfo_screenheight() - h - 50)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.configure(bg="black")

        self.gif_image = Image.open(GIF_PATH)
        self.frames = []
        self.frame_durations = []
        for frame in ImageSequence.Iterator(self.gif_image):
            frame_rgba = frame.convert("RGBA")
            self.frames.append(ImageTk.PhotoImage(frame_rgba.copy()))
            self.frame_durations.append(frame.info.get("duration", 100))

        self.frame_index = 0
        self.label = tk.Label(self.root, bg="black")
        self.label.pack(expand=True, fill="both")
        self._animate_gif()

        if self.user_text:
            txt = tk.Label(
                self.root, text=self.user_text,
                font=("Segoe UI", 11, "italic"), fg="#ffffff",
                bg="black", wraplength=280, justify="center",
            )
            txt.pack(side="bottom", pady=(0, 8))

    def _setup_text_mode(self):
        color = self.data["color"]
        emoji = self.data["emoji"]
        bg = self.data["bg_color"]
        w, h = 420, 280
        x = random.randint(50, self.root.winfo_screenwidth() - w - 50)
        y = random.randint(50, self.root.winfo_screenheight() - h - 50)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.configure(bg=bg)

        container = tk.Frame(self.root, bg=bg)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Frame(container, bg=bg).pack(expand=True)

        emoji_lbl = tk.Label(container, text=emoji, font=("Segoe UI Emoji", 60), fg=color, bg=bg)
        emoji_lbl.pack(pady=(0, 4))

        title_lbl = tk.Label(
            container, text=self.data["label"],
            font=("Segoe UI", 20, "bold"), fg=color, bg=bg,
        )
        title_lbl.pack()

        if self.user_text:
            tk.Frame(container, height=1, bg=color, width=260).pack(pady=(8, 6))
            msg = self.user_text if len(self.user_text) <= 120 else self.user_text[:117] + "..."
            txt_lbl = tk.Label(
                container, text=msg,
                font=("Segoe UI", 12, "italic"), fg="#ffffff",
                bg=bg, wraplength=360, justify="center",
            )
            txt_lbl.pack()

        tk.Frame(container, bg=bg).pack(expand=True)

    def _animate_gif(self):
        if not self.frames:
            return
        self.label.configure(image=self.frames[self.frame_index])
        delay = self.frame_durations[self.frame_index]
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(delay, self._animate_gif)

    def _play_sound(self):
        path = os.path.join(SOUND_DIR, f"{self.reaction_key}.mp3")
        if not os.path.exists(path):
            path = os.path.join(SOUND_DIR, f"{self.reaction_key}.wav")
        if not os.path.exists(path):
            path = DEFAULT_SOUND
        if not os.path.exists(path):
            return
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except Exception:
            pass

    def _start_fadeout(self):
        self._alpha = 1.0
        self._do_fade()

    def _do_fade(self):
        self._alpha -= 0.05
        if self._alpha <= 0:
            self._close()
            return
        try:
            self.root.attributes("-alpha", max(0, self._alpha))
            self.root.after(50, self._do_fade)
        except Exception:
            self._close()

    def _close(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    args = _parse_args()
    app = ReactionWindow(args.reaction, args.text)
    app.run()
