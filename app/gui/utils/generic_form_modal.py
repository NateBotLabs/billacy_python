import tkinter as tk
from tkinter import ttk
from app.gui.utils.constants import ICON_PATH, LOGOUT_ICON_PATH


class GenericFormModal(tk.Toplevel):
    """
    A reusable modal dialog for forms.
    - Pass a window title
    - Pass a fields list: [{"label": "Name", "type": "entry"}, ...]
    - Returns data dict when submitted
    """

    def __init__(self, parent, title="Form", fields=None, on_submit=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.iconbitmap(str(ICON_PATH))
        self.fields = fields or []
        self.entries = {}
        self.on_submit = on_submit

        # Make modal
        self.transient(parent)
        self.grab_set()

        self.build_form()
        self.center_window()

    def build_form(self):
        container = tk.Frame(self)
        container.pack(padx=10, pady=10)

        # Create all form fields dynamically
        for idx, field in enumerate(self.fields):
            label = tk.Label(container, text=field["label"])
            label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")

            entry = tk.Entry(container)
            entry.grid(row=idx, column=1, padx=5, pady=5)

            self.entries[field["label"]] = entry

        # Buttons
        btn_frame = tk.Frame(container)
        btn_frame.grid(columnspan=2, pady=10)

        tk.Button(btn_frame, text="Submit", command=self.submit).grid(
            row=0, column=0, padx=10
        )
        tk.Button(btn_frame, text="Cancel", command=self.destroy).grid(
            row=0, column=1, padx=10
        )

    def submit(self):
        """Collect values and return to callback"""
        data = {
            key: widget.get()
            for key, widget in self.entries.items()
        }

        if self.on_submit:
            self.on_submit(data)

        self.destroy()

    def center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()

        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)

        self.geometry(f"{w}x{h}+{x}+{y}")
