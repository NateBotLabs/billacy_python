import tkinter as tk
from tkinter import ttk

class UsersPage(tk.Frame):
    def __init__(self, parent, user_service, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.user_service = user_service

        label = tk.Label(self, text="Users", font=("Arial", 18))
        label.pack(pady=10)

        # List all users
        self.tree = ttk.Treeview(self, columns=("ID", "First Name", "Last Name", "Email"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        self.load_users()

    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        users = self.user_service.get_all_users()
        for user in users:
            self.tree.insert("", "end", values=(user.id, user.first_name, user.last_name, user.email))
