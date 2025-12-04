import tkinter as tk
from tkinter import ttk

class InvoicesPage(tk.Frame):
    def __init__(self, parent, invoice_service, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.invoice_service = invoice_service

        label = tk.Label(self, text="Invoices", font=("Arial", 18))
        label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "User ID", "Total", "Date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        self.load_invoices()

    def load_invoices(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        invoices = self.invoice_service.get_all_invoices()
        for inv in invoices:
            self.tree.insert("", "end", values=(inv.invoice_id, inv.user_id, inv.total_amount, inv.invoice_date))
