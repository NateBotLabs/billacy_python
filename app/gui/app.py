"""Main GUI application for Billacy."""
import tkinter as tk
from app.connection.setup import DatabaseSetup
from app.gui.pages.dashboard import DashboardPage
from app.gui.pages.student_classes import ClassesPage
from app.gui.pages.users import UsersPage
from app.gui.pages.invoices import InvoicesPage
from app.gui.pages.settings import SettingsPage
from app.services.user_service import UserService
from app.services.invoice_service import InvoiceService
from app.services.student_class_service import StudentClassService
from app.utils.logger import logger


def run_app():
    """Run the main GUI application."""
    # Services
    user_service = UserService()
    invoice_service = InvoiceService()
    student_class_service = StudentClassService()

    # Root window
    root = tk.Tk()
    root.title("Billacy")

    # Container for pages
    container = tk.Frame(root)
    container.pack(side="right", fill="both", expand=True)

    # Navigation frame
    nav_frame = tk.Frame(root)
    nav_frame.pack(side="left", fill="y")

    # Pages
    pages = {}
    pages["Dashboard"] = DashboardPage(
        container, user_service, invoice_service)
    pages["Users"] = UsersPage(container, user_service)
    pages["Invoices"] = InvoicesPage(container, invoice_service)
    pages["Settings"] = SettingsPage(container)
    pages["Student Classes"] = ClassesPage(
        container, student_class_service)

    # Place pages in same location
    for page in pages.values():
        page.grid(row=0, column=0, sticky="nsew")

    # Function to show a page
    def show_page(name):
        pages[name].tkraise()

    # Navigation buttons
    for _idx, (name, page) in enumerate(pages.items()):
        btn = tk.Button(nav_frame, text=name, command=lambda n=name: show_page(n))
        btn.pack(fill="x", pady=2, padx=5)

    # Show default page
    show_page("Dashboard")

    # Close DB session on exit
    def on_close():
        DatabaseSetup.close()
        logger.info("Application shutdown, DB session closed.")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
