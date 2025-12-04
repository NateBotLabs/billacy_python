import tkinter as tk
from tkinter import ttk


class DashboardPage(tk.Frame):
    """Main dashboard showing users and invoices."""

    def __init__(self, parent, user_service, invoice_service, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.user_service = user_service
        self.invoice_service = invoice_service
        label = tk.Label(self, text="Dashboard", font=("Arial", 18))
        label.pack(pady=10)

        # Example summary
        total_users = len(self.user_service.get_all_users())
        total_invoices = len(self.invoice_service.get_all_invoices())
        summary = f"Total Users: {total_users}\nTotal Invoices: {total_invoices}"
        tk.Label(self, text=summary, justify="left").pack(pady=10)
        self.create_widgets()

    def create_widgets(self):
        """Create and layout widgets."""
        # Title
        title = ttk.Label(self, text="Billacy Dashboard",
                          font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Separator
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=5)

        # Users Section
        user_frame = ttk.LabelFrame(self, text="Users")
        user_frame.pack(fill="both", expand=True, padx=10, pady=10)

        users = self.user_service.get_all_users()
        if users:
            for user in users:
                ttk.Label(user_frame, text=f"{user.first_name} {user.last_name} ({user.email})").pack(
                    anchor="w", padx=5, pady=2)
        else:
            ttk.Label(user_frame, text="No users found").pack(
                anchor="w", padx=5, pady=2)

        # Separator
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=5)

        # Invoices Section
        invoice_frame = ttk.LabelFrame(self, text="Invoices")
        invoice_frame.pack(fill="both", expand=True, padx=10, pady=10)

        invoices = self.invoice_service.get_all_invoices()
        if invoices:
            for invoice in invoices:
                ttk.Label(invoice_frame, text=f"Invoice {invoice.invoice_id} - User ID: {invoice.user_id} - Total: {invoice.total_amount}").pack(
                    anchor="w", padx=5, pady=2)
        else:
            ttk.Label(invoice_frame, text="No invoices found").pack(
                anchor="w", padx=5, pady=2)
