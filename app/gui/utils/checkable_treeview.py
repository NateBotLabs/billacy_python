import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Iterable, List, Dict, Optional, Any
from app.gui.utils.style_manager import StyleManager

APP_DIR = Path(__file__).resolve().parents[2]

CHECKED_ICON_PATH = APP_DIR / "assets/images/icons/checkbox_checked.png"
UNCHECKED_ICON_PATH = APP_DIR / "assets/images/icons/checkbox_unchecked.png"
HALFCHECKED_ICON_PATH = APP_DIR / "assets/images/icons/checkbox_halfchecked.png"


class CheckableTreeView(ttk.Frame):
    """
    Reusable Treeview with a checkbox (image) column in #0 and tri-state header.
    """

    def __init__(self, parent, columns: Iterable[str], height: int = 30,
                 on_row_double_click=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.columns: List[str] = list(columns)
        style_manager = StyleManager()

        # Load icons
        self.icon_checked = tk.PhotoImage(file=str(CHECKED_ICON_PATH))
        self.icon_unchecked = tk.PhotoImage(file=str(UNCHECKED_ICON_PATH))
        self.icon_halfchecked = tk.PhotoImage(file=str(HALFCHECKED_ICON_PATH))

        # Save string identifiers for comparison
        self._checked_img_str = str(self.icon_checked)
        self._unchecked_img_str = str(self.icon_unchecked)
        self._half_img_str = str(self.icon_halfchecked)

        # Header checkbox state
        self.header_state = "unchecked"

        # Callback
        self.on_row_double_click = on_row_double_click

        # Treeview widget
        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            show="tree headings",
            height=height,
            selectmode="none"
        )

        # Style: slightly taller rows
        style = ttk.Style()
        style.configure("Custom.Treeview", rowheight=40)
        style.configure("Custom.Treeview.Column0", anchor="center")
        self.tree.configure(style="Custom.Treeview")

        self.tree.pack(fill="both", expand=True)

        # Configure #0 column with checkbox header
        self.tree.column("#0", width=40, anchor="center", stretch=False)
        self.tree.heading("#0", image=self.icon_unchecked)
        self.tree.tag_configure(
            "checked", background=style_manager.nav_bg, foreground=style_manager.nav_fg, anchor="center")

        self.tree.tag_configure("centered_icon", anchor="center")

        # Configure other columns
        for col in self.columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=140, anchor="center")

        # Bind clicks
        self.tree.bind("<Button-1>", self._handle_click)
        if on_row_double_click:
            self.tree.bind("<Double-1>", self._on_double_click)

    # --------------------------
    # Public API
    # --------------------------
    def insert_row(self, id: Any, values: Iterable[Any]):
        iid = str(id)
        vals = list(values)
        if len(vals) < len(self.columns):
            vals += [""] * (len(self.columns) - len(vals))
        self.tree.insert("", "end", iid=iid,
                         image=self.icon_unchecked, values=vals, tags=("centered_icon",))
        self._update_header_checkbox()

    def refresh_list(self, rows: Iterable):
        for child in self.tree.get_children():
            self.tree.delete(child)

        for row in rows:
            if isinstance(row, dict):
                if "id" not in row:
                    raise ValueError("row dict must contain an 'id' key")
                iid = row["id"]
                values = [row.get(col, "") for col in self.columns]
            else:
                seq = list(row)
                if len(seq) == 0:
                    continue
                iid = seq[0]
                values = seq[1:]
            self.insert_row(iid, values)

        self._update_header_checkbox()

    def get_checked(self) -> List[str]:
        checked = []
        for iid in self.tree.get_children():
            img_field = self.tree.item(iid, "image")
            img_str = self._image_field_to_str(img_field)
            if img_str == self._checked_img_str:
                checked.append(iid)
        return checked

    def get_selected_row(self) -> Optional[str]:
        item = self.tree.focus()
        return item if item else None

    def update_row(self, iid: str, values: Optional[Iterable[Any]] = None, checked: Optional[bool] = None):
        if iid not in self.tree.get_children():
            raise ValueError(f"No row with iid={iid}")

        if values is not None:
            vals = list(values)
            if len(vals) < len(self.columns):
                vals += [""] * (len(self.columns) - len(vals))
            self.tree.item(iid, values=vals)

        if checked is not None:
            if checked:
                self.tree.item(iid, image=self.icon_checked, tags=("checked",))
            else:
                self.tree.item(iid, image=self.icon_unchecked, tags=())
        self._update_header_checkbox()

    def update_checked_rows(self, values: Optional[Dict[str, Iterable[Any]]] = None, checked: Optional[bool] = None):
        for iid in self.get_checked():
            row_values = values[iid] if values and iid in values else None
            self.update_row(iid, values=row_values, checked=checked)
        self._update_header_checkbox()

    # --------------------------
    # Internal helpers / events
    # --------------------------
    def _on_double_click(self, event):
        iid = self.get_selected_row()
        if iid and self.on_row_double_click:
            try:
                self.on_row_double_click(iid)
            except Exception:
                pass

    def _handle_click(self, event):
        region = self.tree.identify("region", event.x, event.y)

        # Header click
        if region == "heading":
            col = self.tree.identify_column(event.x)
            if col == "#0":
                self._toggle_select_all()
                return

        # Row click
        if region != "tree":
            return
        row = self.tree.identify_row(event.y)
        if not row:
            return

        img_field = self.tree.item(row, "image")
        img_str = self._image_field_to_str(img_field)

        if img_str == self._unchecked_img_str:
            self.tree.item(row, image=self.icon_checked, tags=("checked",))
        else:
            self.tree.item(row, image=self.icon_unchecked, tags=())

        self._update_header_checkbox()

    @staticmethod
    def _image_field_to_str(img_field) -> str:
        if isinstance(img_field, tuple) and len(img_field) > 0:
            return str(img_field[0])
        return str(img_field)

    # --------------------------
    # Header checkbox logic
    # --------------------------
    def _toggle_select_all(self):
        all_checked = len(self.get_checked()) == len(self.tree.get_children())
        if all_checked:
            # uncheck all
            for iid in self.tree.get_children():
                self.tree.item(iid, image=self.icon_unchecked, tags=("centered_icon"))
        else:
            # check all
            for iid in self.tree.get_children():
                self.tree.item(iid, image=self.icon_checked, tags=("checked", "centered_icon"))
        self._update_header_checkbox()

    def _update_header_checkbox(self):
        total = len(self.tree.get_children())
        checked = len(self.get_checked())

        if checked == 0:
            self.tree.heading("#0", image=self.icon_unchecked)
            self.header_state = "unchecked"
        elif checked == total:
            self.tree.heading("#0", image=self.icon_checked)
            self.header_state = "checked"
        else:
            self.tree.heading("#0", image=self.icon_halfchecked)
            self.header_state = "half"
