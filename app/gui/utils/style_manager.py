# style.py
class StyleManager:
    def __init__(self):
        # Root / Page styles
        self.bg_color = "#f0f0f0"
        self.fg_color = "#000000"
        self.font = ("Segoe UI", 11)

        # Navigation styles
        self.nav_bg = "#2c3e50"
        self.nav_fg = "#ecf0f1"
        self.nav_hover_bg = "#34495e"
        self.nav_active_bg = "#1abc9c"
        self.nav_active_fg = "#ffffff"

    def apply_root_style(self, root):
        root.configure(bg=self.bg_color)

    def apply_page_style(self, frame):
        frame.configure(bg=self.bg_color)
        # apply other widgets dynamically if needed

    def set_theme(self, bg_color=None, fg_color=None, button_color=None, font=None):
        if bg_color:
            self.bg_color = bg_color
        if fg_color:
            self.fg_color = fg_color
        if button_color:
            self.button_color = button_color
        if font:
            self.font = font
