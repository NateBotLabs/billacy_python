import tkinter as tk
from tkinter import ttk

class LoginPage(tk.Frame):
    """Filler login page."""

    def __init__(self, parent, login_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.login_callback = login_callback

        bg_color = "#f0f0f0"
        self.configure(bg=bg_color)
        self.grid(row=0, column=0, sticky="nsew")

        # Center container
        container = tk.Frame(self, bg=bg_color)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Login Page", font=("Arial", 24, "bold"), bg=bg_color).pack(pady=(0,20))
        ttk.Button(container, text="Simulate Login", command=self.simulate_login).pack(padx=20, pady=5)

    def simulate_login(self):
        if self.login_callback:
            self.login_callback()
