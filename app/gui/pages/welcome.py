import tkinter as tk
from tkinter import ttk


class WelcomePage(tk.Frame):
    """Landing page for users who are not logged in."""

    def __init__(self, parent, show_login_callback, show_signup_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.show_login = show_login_callback
        self.show_signup = show_signup_callback

        bg_color = "#f0f0f0"
        self.configure(bg=bg_color)
        self.grid(row=0, column=0, sticky="nsew")

        # Center container for content
        container = tk.Frame(self, bg=bg_color)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = tk.Label(container, text="Welcome to Billacy",
                         font=("Arial", 24, "bold"), bg=bg_color)
        title.pack(pady=(0, 20))

        # Subtitle / description
        subtitle = tk.Label(
            container,
            text="Manage your students, invoices, and classes with ease.",
            font=("Arial", 12),
            bg=bg_color
        )
        subtitle.pack(pady=(0, 30))

        # Buttons
        login_btn = ttk.Button(container, text="Log In",
                               command=self.show_login)
        login_btn.pack(fill="x", padx=20, pady=5)

        signup_btn = ttk.Button(
            container, text="Sign Up", command=self.show_signup)
        signup_btn.pack(fill="x", padx=20, pady=5)
