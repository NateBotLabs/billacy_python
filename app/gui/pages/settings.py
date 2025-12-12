import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from app.services.settings_service import SettingsService
from pathlib import Path


class SettingsPage(tk.Frame):
    CACHE_DIR = Path(".cache/media")

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.service = SettingsService()

        tk.Label(self, text="Settings", font=("Arial", 18)).pack(pady=10)

        # Profile photo
        tk.Label(self, text="Profile Photo").pack(pady=5)
        self.profile_label = tk.Label(self)
        self.profile_label.pack(pady=5)
        tk.Button(self, text="Upload Profile Photo",
                  command=self.upload_profile_photo).pack(pady=5)

        # Documents
        tk.Label(self, text="Documents").pack(pady=5)
        self.documents_frame = tk.Frame(self)
        self.documents_frame.pack(pady=5)
        tk.Button(self, text="Upload Document",
                  command=self.upload_document).pack(pady=5)

        # Other media
        tk.Label(self, text="Other Media").pack(pady=5)
        self.other_media_frame = tk.Frame(self)
        self.other_media_frame.pack(pady=5)
        tk.Button(self, text="Upload Other Media",
                  command=self.upload_other_media).pack(pady=5)

        self.refresh_media()

    def refresh_media(self):
        # Profile photo

        media = self.service.get_profile_photo()
        if media:
            local_path = self.CACHE_DIR / media.original_filename
            try:
                self.service.download_profile_photo(local_path)
                img = Image.open(local_path).resize((100, 100))
                self.profile_img = ImageTk.PhotoImage(img)
                self.profile_label.config(image=self.profile_img, text="")
            except Exception as e:
                self.profile_label.config(text=f"Failed to load image: {e}")
        else:
            self.profile_label.config(image="", text="No profile photo")

        # Documents
        for w in self.documents_frame.winfo_children():
            w.destroy()
        for doc in self.service.get_documents():
            tk.Label(self.documents_frame,
                     text=doc.original_filename).pack(anchor="w")

        # Other media
        for w in self.other_media_frame.winfo_children():
            w.destroy()
        for media in self.service.get_other_media():
            tk.Label(self.other_media_frame,
                     text=media.original_filename).pack(anchor="w")

    # ------------------------
    # Upload handlers
    # ------------------------
    def upload_profile_photo(self):
        file_path = filedialog.askopenfilename(title="Select Profile Photo",
                                               filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            try:
                self.service.upload_profile_photo(file_path)
                messagebox.showinfo("Success", "Profile photo uploaded!")
                self.refresh_media()
            except Exception as e:
                messagebox.showerror("Error", f"Upload failed: {e}")

    def upload_document(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Documents",
            filetypes=[("PDF/Images", "*.pdf *.jpg *.jpeg *.png")]
        )
        if file_paths:
            failed = []
            for file_path in file_paths:
                try:
                    self.service.upload_document(file_path)
                except Exception as e:
                    failed.append((file_path, str(e)))

            if not failed:
                messagebox.showinfo("Success", "All documents uploaded!")
            else:
                msg = "\n".join(f"{fp}: {err}" for fp, err in failed)
                messagebox.showwarning(
                    "Partial Success", f"Some uploads failed:\n{msg}")

            self.refresh_media()

    def upload_other_media(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Media",
            filetypes=[
                ("All Media", "*.jpg *.jpeg *.png *.gif *.mp3 *.mp4 *.pdf")]
        )
        if file_paths:
            failed = []
            for file_path in file_paths:
                try:
                    self.service.upload_other_media(file_path)
                except Exception as e:
                    failed.append((file_path, str(e)))

            if not failed:
                messagebox.showinfo("Success", "All media uploaded!")
            else:
                msg = "\n".join(f"{fp}: {err}" for fp, err in failed)
                messagebox.showwarning(
                    "Partial Success", f"Some uploads failed:\n{msg}")

            self.refresh_media()
