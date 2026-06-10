import sys
import os
import argparse
import random
import tkinter as tk
import pygame

from triggers import TRIGGERS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(SCRIPT_DIR, "sounds")
DEFAULT_SOUND = os.path.join(SCRIPT_DIR, "mimimi-clash-royale.mp3")


def _parse_args():
    parser = argparse.ArgumentParser(description="Mi-Mi-Mi Reaction Window")
    parser.add_argument("--reaction", default="mimimi", help="Ключ реакции (mimimi, bravo, etc.)")
    parser.add_argument("--text", default="", help="Текст от пользователя")
    return parser.parse_args()


def _get_window_size(reaction: str, text: str) -> tuple:
    base_w, base_h = 420, 300
    if text:
        lines = text.count("\n") + 1
        extra = min(lines * 24, 200)
        base_h += extra
    return base_w, base_h


class ReactionWindow:
    def __init__(self, reaction: str, text: str):
        args = _parse_args()
        self.reaction_key = reaction
        self.reaction_data = TRIGGERS.get(reaction, TRIGGERS["mimimi"])
        self.user_text = text

        self.root = tk.Tk()
        w, h = _get_window_size(reaction, text)
        self.root.geometry(self._random_geometry(w, h))
        self.root.title(self.reaction_data["label"])
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.root.configure(bg=self.reaction_data["bg_color"])
        self.root.overrideredirect(True)

        self._draw()

        self._play_sound()
        self.root.after(2500, self._start_fadeout)

    def _random_geometry(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = random.randint(50, sw - w - 50)
        y = random.randint(50, sh - h - 50)
        return f"{w}x{h}+{x}+{y}"

    def _draw(self):
        data = self.reaction_data
        color = data["color"]
        emoji = data["emoji"]
        bg = data["bg_color"]

        container = tk.Frame(self.root, bg=bg)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Frame(container, bg=bg).pack(expand=True)

        emoji_lbl = tk.Label(container, text=emoji, font=("Segoe UI Emoji", 64), fg=color, bg=bg)
        emoji_lbl.pack(pady=(0, 6))

        title_lbl = tk.Label(
            container, text=data["label"],
            font=("Segoe UI", 22, "bold"), fg=color, bg=bg,
        )
        title_lbl.pack()

        if self.user_text:
            tk.Frame(container, height=1, bg=color, width=280).pack(pady=(10, 8))
            msg = self.user_text if len(self.user_text) <= 120 else self.user_text[:117] + "..."
            txt_lbl = tk.Label(
                container, text=msg,
                font=("Segoe UI", 13, "italic"), fg="#ffffff",
                bg=bg, wraplength=360, justify="center",
            )
            txt_lbl.pack()

        tk.Frame(container, bg=bg).pack(expand=True)

        close_btn = tk.Label(
            container, text="✕", font=("Segoe UI", 12),
            fg=color, bg=bg, cursor="hand2",
        )
        close_btn.pack(side="bottom", anchor="se")
        close_btn.bind("<Button-1>", lambda e: self._close())

        self.root.bind("<Escape>", lambda e: self._close())
        self.root.bind("<Button-1>", lambda e: self._close())

    def _play_sound(self):
        sound_path = os.path.join(SOUND_DIR, f"{self.reaction_key}.mp3")
        if not os.path.exists(sound_path):
            sound_path = os.path.join(SOUND_DIR, f"{self.reaction_key}.wav")
        if not os.path.exists(sound_path):
            sound_path = DEFAULT_SOUND

        if not os.path.exists(sound_path):
            return

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except Exception:
            pass

    def _start_fadeout(self):
        self._fade_step = 1.0
        self._fade()

    def _fade(self):
        self._fade_step -= 0.05
        if self._fade_step <= 0:
            self._close()
            return
        self.root.attributes("-alpha", max(0, self._fade_step))
        self.root.after(50, self._fade)

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
