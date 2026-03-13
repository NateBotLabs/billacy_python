"""Main GUI application for Billacy."""
import tkinter as tk
from pathlib import Path
from app.connection.setup import DatabaseSetup
from app.gui.pages.dashboard import DashboardPage
from app.gui.pages.student_classes import ClassesPage
from app.gui.pages.items import ItemsPage
from app.gui.pages.welcome import WelcomePage
from app.gui.pages.auth.login import LoginPage
from app.gui.pages.auth.sign_up import SignupPage
from app.gui.pages.users import UsersPage
from app.gui.pages.invoices import InvoicesPage
from app.gui.pages.settings import SettingsPage
from app.services.user_service import UserService
from app.services.invoice_service import InvoiceService
from app.services.student_class_service import StudentClassService
from app.services.item_service import ItemService
from app.gui.utils.style_manager import StyleManager
from app.utils.logger import logger
from app.gui.utils.constants import ICON_PATH, LOGOUT_ICON_PATH


APP_DIR = Path(__file__).resolve().parent.parent  # adjust to root of app
icon_images = {}


def run_app():
    """Run the main GUI application."""
    # Services
    user_service = UserService()
    invoice_service = InvoiceService()
    student_class_service = StudentClassService()
    items_class_service = ItemService()
    logged_in = False

    # Root window
    root = tk.Tk()
    root.state("zoomed")
    style = StyleManager()
    style.apply_root_style(root)
    root.title("Billacy")
    root.iconbitmap(str(ICON_PATH))

    # Container for pages
    container = tk.Frame(root)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    container.pack(side="right", fill="both", expand=True)

    # Navigation frame (hidden initially)
    nav_frame = tk.Frame(root, bg=style.nav_bg, width=150)

    # Pages dictionary
    pages = {}

    # Active nav tracking
    nav_buttons = {}
    active_btn = None

    # Login callback
    def on_login():
        nonlocal logged_in
        logged_in = True
        nav_frame.pack(side="left", fill="y")
        show_page("Dashboard")

    # Function to show a page
    def show_page(name):
        nonlocal active_btn
        pages[name].tkraise()
        # Highlight nav buttons only if in nav
        if name in nav_buttons:
            if active_btn:
                active_btn.configure(bg=style.nav_bg, fg=style.nav_fg)
            nav_buttons[name].configure(
                bg=style.nav_active_bg, fg=style.nav_active_fg)
            active_btn = nav_buttons[name]

    # Pre-login pages
    pages["Welcome"] = WelcomePage(
        container,
        show_login_callback=lambda: show_page("Login"),
        show_signup_callback=lambda: show_page("SignUp")
    )
    pages["Welcome"].grid(row=0, column=0, sticky="nsew")

    pages["Login"] = LoginPage(container, login_callback=on_login)
    pages["Login"].grid(row=0, column=0, sticky="nsew")

    pages["SignUp"] = SignupPage(container, signup_callback=on_login)
    pages["SignUp"].grid(row=0, column=0, sticky="nsew")

    # Main pages (created once)
    main_pages = {
        "Dashboard": DashboardPage(container, user_service, invoice_service),
        "Users": UsersPage(container, user_service, student_class_service),
        "Invoices": InvoicesPage(container, invoice_service, user_service),
        "Classes": ClassesPage(container, student_class_service),
        "Items": ItemsPage(container, items_class_service),
        "Settings": SettingsPage(container)
    }
    pages.update(main_pages)
    for page in main_pages.values():
        page.grid(row=0, column=0, sticky="nsew")

    # Create nav buttons (once)
    top_spacer = tk.Frame(nav_frame, bg=style.nav_bg)
    top_spacer.pack(expand=True, fill="y")

    icon_paths = {
        "Dashboard": APP_DIR / "assets/images/icons/dashboard.png",
        "Users": APP_DIR / "assets/images/icons/users.png",
        "Items": APP_DIR / "assets/images/icons/items.png",
        "Invoices": APP_DIR / "assets/images/icons/invoices.png",
        "Classes": APP_DIR / "assets/images/icons/classes.png",
        "Settings": APP_DIR / "assets/images/icons/settings.png"
    }

    for name in main_pages:
        icon = tk.PhotoImage(file=str(icon_paths[name]))
        icon_images[name] = icon
        btn = tk.Button(
            nav_frame,
            text=name,
            anchor="w",
            image=icon_images[name],
            compound="left",
            bg=style.nav_bg,
            fg=style.nav_fg,
            font=style.font,
            relief="flat",
            command=lambda n=name: show_page(n)
        )
        btn.pack(fill="x", pady=3, padx=5)

        btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=style.nav_hover_bg))
        btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=style.nav_bg))

        nav_buttons[name] = btn

    bottom_spacer = tk.Frame(nav_frame, bg=style.nav_bg)
    bottom_spacer.pack(expand=True, fill="y")
    logout_icon = tk.PhotoImage(file=str(LOGOUT_ICON_PATH))
    logout_btn = tk.Button(
        nav_frame,
        text="Logout",
        anchor="w",
        image=logout_icon,   # <-- MUST use stored image
        compound="left",
        bg=style.nav_bg,
        fg=style.nav_fg,
        font=style.font,
        relief="flat",
        command=lambda: on_logout()
    )
    logout_btn.pack(fill="x", pady=3, padx=5)
    logout_btn.bind("<Enter>", lambda e: logout_btn.configure(
        bg=style.nav_hover_bg))
    logout_btn.bind("<Leave>", lambda e: logout_btn.configure(bg=style.nav_bg))

    # Initially hide nav
    nav_frame.pack_forget()

    # Logout callback
    def on_logout():
        nonlocal logged_in
        logged_in = False
        nav_frame.pack_forget()
        show_page("Welcome")

    # Show Welcome page by default
    show_page("Welcome")

    # Close DB session on exit
    def on_close():
        DatabaseSetup.close()
        logger.info("Application shutdown, DB session closed.")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
