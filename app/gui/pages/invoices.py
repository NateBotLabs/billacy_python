import tkinter as tk
from tkinter import messagebox
from app.gui.utils.checkable_treeview import CheckableTreeView
from app.gui.utils.generic_form_modal import GenericFormModal
from app.gui.utils.constants import ADD_ICON_PATH, DELETE_ICON_PATH
from app.utils.logger import logger


class InvoicesPage(tk.Frame):
    def __init__(self, parent, invoice_service, user_service, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.invoice_service = invoice_service
        self.user_service = user_service

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Invoices", font=("Arial", 18)).grid(
            row=0, column=0, pady=10
        )

        # -------------------------
        # Buttons
        # -------------------------
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
            text=" Add Invoice",
            compound="left",
            command=self.add_invoice
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text=" Edit Selected",
            command=self.edit_invoice
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            image=self.delete_icon,
            text=" Remove Selected",
            compound="left",
            command=self.remove_invoice
        ).grid(row=0, column=2, padx=5)

        # -------------------------
        # CheckableTreeView
        # -------------------------
        self.tree = CheckableTreeView(
            self,
            columns=["ID", "User", "Total", "Date"],
            height=30
        )
        self.tree.grid(row=2, column=0, sticky="nsew", pady=10)

        self.refresh_list()

    # -------------------------
    # Refresh list
    # -------------------------
    def refresh_list(self):
        invoices = self.invoice_service.get_all_invoices()
        rows = []
        for inv in invoices:
            user_name = "-"
            if inv.user_id:
                user = self.user_service.get_user(inv.user_id)
                user_name = f"{user.first_name} {user.last_name}" if user else "-"

            rows.append({
                "id": inv.invoice_id,
                "ID": inv.invoice_id,
                "User": user_name,
                "Total": inv.total_amount,
                "Date": inv.invoice_date,
            })

        self.tree.refresh_list(rows)

    # -------------------------
    # Add invoice modal
    # -------------------------
    def add_invoice(self):
        # Example: simple modal with User dropdown
        users = self.user_service.get_all_users()
        user_names = [f"{u.first_name} {u.last_name}" for u in users]
        user_map = {f"{u.first_name} {u.last_name}": u.id for u in users}

        def handle_submit(data):
            try:
                user_id = user_map.get(data["User"])
                self.invoice_service.create_invoice(
                    user_id=user_id, total_amount=data["Total"])
                messagebox.showinfo("Success", "Invoice created!")
                self.refresh_list()
            except Exception as e:
                logger.error(f"Failed to add invoice: {e}")
                messagebox.showerror("Error", str(e))

        fields = [
            {"label": "User", "options": user_names},
            {"label": "Total"}
        ]

        GenericFormModal(self, title="Add Invoice",
                         fields=fields, on_submit=handle_submit)

    # -------------------------
    # Edit invoice modal
    # -------------------------
    def edit_invoice(self):
        checked = self.tree.get_checked()
        if not checked:
            messagebox.showwarning("Select", "Select an invoice to edit.")
            return

        iid = checked[0]
        item = self.tree.tree.item(iid)
        data = dict(zip(["ID", "User", "Total", "Date"], item["values"]))

        users = self.user_service.get_all_users()
        user_names = [f"{u.first_name} {u.last_name}" for u in users]
        user_map = {f"{u.first_name} {u.last_name}": u.id for u in users}

        def handle_submit(submit_data):
            try:
                user_id = user_map.get(submit_data["User"])
                updated_invoice = self.invoice_service.edit_invoice(
                    invoice_id=iid,
                    user_id=user_id,
                    total_amount=submit_data["Total"]
                )

                # Update row
                self.tree.update_row(
                    iid,
                    values=[
                        updated_invoice.invoice_id,
                        submit_data["User"],
                        updated_invoice.total_amount,
                        updated_invoice.invoice_date
                    ]
                )
                messagebox.showinfo("Success", "Invoice updated!")
            except Exception as e:
                logger.error(f"Failed to update invoice: {e}")
                messagebox.showerror("Error", str(e))

        fields = [
            {"label": "User", "value": data["User"], "options": user_names},
            {"label": "Total", "value": data["Total"]},
        ]

        GenericFormModal(self, title="Edit Invoice",
                         fields=fields, on_submit=handle_submit)

    # -------------------------
    # Remove invoice
    # -------------------------
    def remove_invoice(self):
        checked_ids = self.tree.get_checked()
        if not checked_ids:
            messagebox.showwarning("Select", "Select at least one invoice.")
            return

        for invoice_id in checked_ids:
            try:
                self.invoice_service.delete_invoice(invoice_id)
            except Exception as e:
                logger.error(f"Failed to delete invoice {invoice_id}: {e}")

        messagebox.showinfo("Deleted", "Selected invoices removed.")
        self.refresh_list()
