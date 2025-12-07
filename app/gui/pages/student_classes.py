import tkinter as tk
from tkinter import messagebox
from app.utils.logger import logger
from app.gui.utils.generic_form_modal import GenericFormModal
from app.gui.utils.checkable_treeview import CheckableTreeView
from app.gui.utils.constants import ADD_ICON_PATH, DELETE_ICON_PATH


class ClassesPage(tk.Frame):
    def __init__(self, parent, classes_service, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.classes_service = classes_service

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Student Classes",
                 font=("Arial", 18)).grid(row=0, column=0, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=1, column=0, pady=5)

        try:
            self.add_icon = tk.PhotoImage(file=ADD_ICON_PATH)
            self.delete_icon = tk.PhotoImage(file=DELETE_ICON_PATH)
        except Exception:
            self.add_icon = None
            self.delete_icon = None

        tk.Button(
            btn_frame,
            image=self.add_icon,
            text=" Add Student Class",
            compound="left",
            command=self.add_class
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text=" Edit Selected",
            command=self.edit_class
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            btn_frame,
            image=self.delete_icon,
            text=" Remove Selected",
            compound="left",
            command=self.remove_class
        ).grid(row=0, column=1, padx=5)

        # --- Checkable TreeView (REUSABLE COMPONENT) ---
        self.tree = CheckableTreeView(
            self,
            columns=["ID", "Name", "Description", "Tutor", "Tuition Fee"],
            height=12
        )
        self.tree.grid(row=2, column=0, sticky="nsew", pady=10)

        self.refresh_list()

    # -------------------------------------------------
    # Refresh list
    # -------------------------------------------------
    def refresh_list(self):
        classes = self.classes_service.get_all_classes()

        rows = []
        for cls in classes:
            rows.append({
                "id": cls.id,
                "ID": cls.id,
                "Name": cls.name,
                "Description": cls.description,
                "Tutor": cls.tutor,
                "Tuition Fee": f"{cls.tuition_fee:.2f}",
            })

        self.tree.refresh_list(rows)

    # -------------------------------------------------
    # Add class modal
    # -------------------------------------------------
    def add_class(self):
        def handle_submit(data):
            try:
                new_class = self.classes_service.create_student_class(
                    name=data["Name"],
                    description=data["Description"],
                    tutor=data["Tutor"],
                    tuition_fee=float(data["Tuition Fee"], 2)
                )
                messagebox.showinfo(
                    "Success", f"Class '{new_class.name}' added!")
                self.refresh_list()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logger.error(f"Failed to add class: {e}")

        fields = [
            {"label": "Name"},
            {"label": "Description"},
            {"label": "Tutor"},
            {"label": "Tuition Fee"},
        ]

        GenericFormModal(self, title="Add Student Class",
                         fields=fields, on_submit=handle_submit)

    # -------------------------------------------------
    # Remove selected classes
    # -------------------------------------------------
    def remove_class(self):
        checked_ids = self.tree.get_checked()  # now simply returns ID strings

        if not checked_ids:
            messagebox.showwarning(
                "Select", "Select at least one class to remove.")
            return

        for class_id in checked_ids:
            try:
                self.classes_service.delete_student_classes(class_id)
            except Exception as e:
                logger.error(f"Failed to delete class id={class_id}: {e}")
                messagebox.showerror(
                    "Error", f"Failed to delete class ID {class_id}")

        messagebox.showinfo(
            "Deleted", "Selected classes removed successfully.")
        self.refresh_list()

    def edit_class(self):
        checked_iids = self.tree.get_checked()
        if not checked_iids:
            messagebox.showwarning(
                "Select", "Select at least one class using the checkboxes to edit.")
            return

        # For simplicity, let's only edit the first checked row
        iid = checked_iids[0]

        # Get current values
        item = self.tree.tree.item(iid)
        current_values = item["values"]
        data_initial = dict(
            zip(["ID", "Name", "Description", "Tutor", "Tuition Fee"], current_values))

        def handle_submit(data):
            try:
                updated_class = self.classes_service.update_student_class(
                    class_id=iid,
                    name=data["Name"],
                    description=data["Description"],
                    tutor=data["Tutor"],
                    tuition_fee=float(data["Tuition Fee"])
                )

                # Update row in treeview
                self.tree.update_row(
                    iid,
                    values=[updated_class.id, updated_class.name, updated_class.description,
                            updated_class.tutor, f"{updated_class.tuition_fee:.2f}"]
                )

                messagebox.showinfo(
                    "Success", f"Class '{updated_class.name}' updated!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logger.error(f"Failed to update class id={iid}: {e}")

        fields = [
            {"label": "Name", "value": data_initial["Name"]},
            {"label": "Description", "value": data_initial["Description"]},
            {"label": "Tutor", "value": data_initial["Tutor"]},
            {"label": "Tuition Fee", "value": data_initial["Tuition Fee"]},
        ]

        GenericFormModal(self, title="Edit Student Class",
                         fields=fields, on_submit=handle_submit)
