import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from app.utils.logger import logger

class ClassesPage(tk.Frame):
    def __init__(self, parent, classes_service, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.classes_service = classes_service

        # --- Title ---
        tk.Label(self, text="Student Classes", font=("Arial", 18)).pack(pady=10)

        # --- Form entries ---
        form_frame = tk.Frame(self)
        form_frame.pack(pady=5, fill="x")

        tk.Label(form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(form_frame, text="Description").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(form_frame, text="Tutor").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(form_frame, text="Tuition Fee").grid(row=3, column=0, padx=5, pady=5)

        self.name_entry = tk.Entry(form_frame)
        self.desc_entry = tk.Entry(form_frame)
        self.tutor_entry = tk.Entry(form_frame)
        self.fee_entry = tk.Entry(form_frame)

        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        self.tutor_entry.grid(row=2, column=1, padx=5, pady=5)
        self.fee_entry.grid(row=3, column=1, padx=5, pady=5)

        # --- Buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Class", command=self.add_class).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Remove Selected", command=self.remove_class).grid(row=0, column=1, padx=5)

        # --- Treeview for classes ---
        self.tree = ttk.Treeview(
            self, columns=("ID", "Name", "Description", "Tutor", "Tuition Fee"),
            show="headings", height=10
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10, fill="both", expand=True)

        # --- Load initial classes ---
        self.refresh_list()

    # --- Methods ---
    def refresh_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        classes = self.classes_service.get_all_classes()
        for cls in classes:
            self.tree.insert("", "end", values=(
                getattr(cls, "id", ""),
                cls.name,
                cls.description,
                cls.tutor,
                cls.tuition_fee
            ))

    def add_class(self):
        try:
            new_class = self.classes_service.create_class(
                name=self.name_entry.get(),
                description=self.desc_entry.get(),
                tutor=self.tutor_entry.get(),
                tuition_fee=float(self.fee_entry.get())
            )
            messagebox.showinfo("Success", f"Class '{new_class.name}' added!")
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.error(f"Failed to add class: {e}")


    def remove_class(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a class to remove.")
            return
        item = self.tree.item(selected[0])
        class_id = item["values"][0]
        try:
            self.classes_service.delete_student_class([class_id])
            messagebox.showinfo("Deleted", f"Class '{item['values'][1]}' removed!")
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logger.error(f"Failed to remove class: {e}")