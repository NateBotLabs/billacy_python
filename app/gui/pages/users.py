import tkinter as tk
from tkinter import ttk, messagebox
from app.gui.utils.checkable_treeview import CheckableTreeView
from app.gui.utils.generic_form_modal import GenericFormModal
from app.gui.utils.constants import ADD_ICON_PATH, DELETE_ICON_PATH
from app.utils.logger import logger


class UsersPage(tk.Frame):
    def __init__(self, parent, user_service, classes_service, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.user_service = user_service
        self.classes_service = classes_service

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Users", font=("Arial", 18)).grid(
            row=0, column=0, pady=10
        )

        # ----------------------------------
        # Buttons (same style as ClassesPage)
        # ----------------------------------
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
            text=" Add User",
            compound="left",
            command=self.add_user
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text=" Edit Selected",
            command=self.edit_user
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            image=self.delete_icon,
            text=" Remove Selected",
            compound="left",
            command=self.remove_user
        ).grid(row=0, column=2, padx=5)

        # -------------------------------------------------
        # CheckableTreeView with student class column
        # -------------------------------------------------
        self.tree = CheckableTreeView(
            self,
            columns=["ID", "First Name", "Last Name", "Email", "Class"],
            height=30
        )
        self.tree.grid(row=2, column=0, sticky="nsew", pady=10)

        self.refresh_list()

    # -------------------------------------------------
    # Refresh list
    # -------------------------------------------------
    def refresh_list(self):
        users = self.user_service.get_all_users()

        rows = []
        for user in users:
            attached_class = (
                user.student_class.name if getattr(
                    user, "student_class", None) else "-"
            )

            rows.append({
                "id": user.id,
                "ID": user.id,
                "First Name": user.first_name,
                "Last Name": user.last_name,
                "Email": user.email,
                "Class": attached_class,
            })

        self.tree.refresh_list(rows)

    # -------------------------------------------------
    # Add user modal
    # -------------------------------------------------
    def add_user(self):
        # Load available classes (names only)
        classes = self.classes_service.get_all_classes()
        class_names = [cls.name for cls in classes]

        class_map = {cls.name: cls.id for cls in classes}

        def handle_submit(data):
            try:
                class_id = class_map.get(data["Class"])  # Convert name → id
                new_user = self.user_service.create_user(
                    first_name=data["First Name"],
                    last_name=data["Last Name"],
                    email=data["Email"],
                    class_id=class_id
                )
                messagebox.showinfo("Success", "User created!")
                self.refresh_list()
            except Exception as e:
                logger.error(f"Failed to add user: {e}")
                messagebox.showerror("Error", str(e))

        fields = [
            {"label": "First Name"},
            {"label": "Last Name"},
            {"label": "Email"},
            {"label": "Class", "options": class_names},  # dropdown
        ]

        GenericFormModal(self, title="Add User",
                         fields=fields, on_submit=handle_submit)

    # -------------------------------------------------
    # Edit user modal
    # -------------------------------------------------
    def edit_user(self):
        checked = self.tree.get_checked()
        if not checked:
            messagebox.showwarning("Select", "Select a user to edit.")
            return

        iid = checked[0]
        item = self.tree.tree.item(iid)
        data = dict(zip(["ID", "First Name", "Last Name",
                         "Email", "Class"], item["values"]))

        # All class names
        classes = self.classes_service.get_all_classes()
        class_names = [cls.name for cls in classes]
        class_map = {cls.name: cls.id for cls in classes}

        def handle_submit(submit_data):
            try:
                class_id = class_map.get(
                    submit_data["Class"])  # Convert name → id
                updated_user = self.user_service.edit_user(
                    user_id=iid,
                    first_name=submit_data["First Name"],
                    last_name=submit_data["Last Name"],
                    email=submit_data["Email"],
                    class_id=class_id
                )

                # Update row immediately
                attached_class = (
                    updated_user.student_class.name
                    if getattr(updated_user, "student_class", None)
                    else "-"
                )

                self.tree.update_row(
                    iid,
                    values=[
                        updated_user.id,
                        updated_user.first_name,
                        updated_user.last_name,
                        updated_user.email,
                        attached_class
                    ]
                )

                messagebox.showinfo("Success", "User updated!")
            except Exception as e:
                logger.error(f"Failed to update user: {e}")
                messagebox.showerror("Error", str(e))

        fields = [
            {"label": "First Name", "value": data["First Name"]},
            {"label": "Last Name", "value": data["Last Name"]},
            {"label": "Email", "value": data["Email"]},
            {"label": "Class", "value": data["Class"], "options": class_names},
        ]

        GenericFormModal(self, title="Edit User",
                         fields=fields, on_submit=handle_submit)

    # -------------------------------------------------
    # Remove user
    # -------------------------------------------------
    def remove_user(self):
        checked_ids = self.tree.get_checked()

        if not checked_ids:
            messagebox.showwarning("Select", "Select at least one user.")
            return

        for user_id in checked_ids:
            try:
                self.user_service.delete_user(user_id)
            except Exception as e:
                logger.error(f"Failed to delete user {user_id}: {e}")

        messagebox.showinfo("Deleted", "Selected users removed.")
        self.refresh_list()
