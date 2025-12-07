import tkinter as tk
from tkinter import ttk

class SignupPage(tk.Frame):
    """Filler sign up page."""

    def __init__(self, parent, signup_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.signup_callback = signup_callback

        bg_color = "#f0f0f0"
        self.configure(bg=bg_color)
        self.grid(row=0, column=0, sticky="nsew")

        # Center container
        container = tk.Frame(self, bg=bg_color)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Sign Up Page", font=("Arial", 24, "bold"), bg=bg_color).pack(pady=(0,20))
        ttk.Button(container, text="Simulate Sign Up", command=self.simulate_signup).pack(padx=20, pady=5)

    def simulate_signup(self):
        if self.signup_callback:
            self.signup_callback()
