import tkinter as tk

class SettingsPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        label = tk.Label(self, text="Settings", font=("Arial", 18))
        label.pack(pady=10)

        tk.Label(self, text="Settings page content goes here").pack(pady=10)
