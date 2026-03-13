import tkinter as tk
from tkinter import messagebox
from app.utils.logger import logger
from app.gui.utils.generic_form_modal import GenericFormModal
from app.gui.utils.checkable_treeview import CheckableTreeView
from app.gui.utils.constants import ADD_ICON_PATH, DELETE_ICON_PATH


class ItemsPage(tk.Frame):
    def __init__(self, parent, item_service, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.item_service = item_service

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Items", font=("Arial", 18))\
            .grid(row=0, column=0, pady=10)

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
            text=" Add Item",
            compound="left",
            command=self.add_item
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text=" Edit Selected",
            command=self.edit_item
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            image=self.delete_icon,
            text=" Remove Selected",
            compound="left",
            command=self.remove_item
        ).grid(row=0, column=2, padx=5)

        self.tree = CheckableTreeView(
            self,
            columns=["ID", "Name", "Quantity", "Price"],
            height=30
        )
        self.tree.grid(row=2, column=0, sticky="nsew", pady=10)

        self.refresh_list()

    # -------------------------------------------------
    # Refresh list
    # -------------------------------------------------
    def refresh_list(self):
        items = self.item_service.get_all_items()

        rows = []
        for item in items:
            rows.append({
                "id": item.id,
                "ID": item.id,
                "Name": item.name,
                "Quantity": item.quantity,
                "Price": f"{item.price:.2f}",
            })

        self.tree.refresh_list(rows)

    # -------------------------------------------------
    # Add item
    # -------------------------------------------------
    def add_item(self):
        def handle_submit(data):
            try:
                new_item = self.item_service.create_item(
                    name=data["Name"],
                    quantity=int(data["Quantity"]),
                    price=float(data["Price"])
                )
                messagebox.showinfo(
                    "Success", f"Item '{new_item.name}' added!")
                self.refresh_list()
            except Exception as e:
                logger.error(f"Failed to add item: {e}")
                messagebox.showerror("Error", str(e))

        fields = [
            {"label": "Name"},
            {"label": "Quantity"},
            {"label": "Price"},
        ]

        GenericFormModal(
            self,
            title="Add Item",
            fields=fields,
            on_submit=handle_submit
        )

    # -------------------------------------------------
    # Remove items (soft delete)
    # -------------------------------------------------
    def remove_item(self):
        checked_ids = self.tree.get_checked()

        if not checked_ids:
            messagebox.showwarning(
                "Select", "Select at least one item to remove.")
            return

        try:
            self.item_service.delete_items(checked_ids)
            messagebox.showinfo(
                "Deleted", "Selected items removed successfully.")
            self.refresh_list()
        except Exception as e:
            logger.error(f"Failed to delete items: {e}")
            messagebox.showerror("Error", "Failed to delete items.")

    # -------------------------------------------------
    # Edit item
    # -------------------------------------------------
    def edit_item(self):
        checked_iids = self.tree.get_checked()
        if not checked_iids:
            messagebox.showwarning(
                "Select", "Select an item using the checkbox to edit.")
            return

        iid = checked_iids[0]
        item = self.tree.tree.item(iid)
        current_values = item["values"]

        data_initial = dict(
            zip(["ID", "Name", "Quantity", "Price"], current_values)
        )

        def handle_submit(data):
            try:
                updated_item = self.item_service.edit_item(
                    item_id=iid,
                    name=data["Name"],
                    quantity=int(data["Quantity"]),
                    price=float(data["Price"])
                )

                self.tree.update_row(
                    iid,
                    values=[
                        updated_item.id,
                        updated_item.name,
                        updated_item.quantity,
                        f"{updated_item.price:.2f}"
                    ]
                )

                messagebox.showinfo(
                    "Success", f"Item '{updated_item.name}' updated!")
            except Exception as e:
                logger.error(f"Failed to update item id={iid}: {e}")
                messagebox.showerror("Error", str(e))

        fields = [
            {"label": "Name", "value": data_initial["Name"]},
            {"label": "Quantity", "value": data_initial["Quantity"]},
            {"label": "Price", "value": data_initial["Price"]},
        ]

        GenericFormModal(
            self,
            title="Edit Item",
            fields=fields,
            on_submit=handle_submit
        )
