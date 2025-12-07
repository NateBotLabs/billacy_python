import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Iterable, List, Dict, Optional, Any

APP_DIR = Path(__file__).resolve().parents[2]

CHECKED_ICON_PATH = APP_DIR / "assets/images/icons/checkbox_checked.png"
UNCHECKED_ICON_PATH = APP_DIR / "assets/images/icons/checkbox_unchecked.png"


class CheckableTreeView(ttk.Frame):
    """
    Reusable Treeview with a checkbox (image) column in #0.
    - `columns` is a list of column names shown as headings.
    - `refresh_list(rows)` accepts either:
        * list of dicts where each dict MUST contain "id" and keys matching `columns`
        * list of tuples/lists where first item is id and remaining items match `columns`
    - `insert_row(id, values)` accepts values sequence matching the columns order.
    - `get_checked()` returns list of iids (string ids) that are checked.
    - Optional `on_row_double_click` receives the iid of the focused row.
    """

    def __init__(self, parent, columns: Iterable[str], height: int = 12,
                 on_row_double_click=None, **kwargs):
        super().__init__(parent, **kwargs)

        # Store columns in order (list)
        self.columns: List[str] = list(columns)

        # Load icons and keep references to avoid GC
        self.icon_checked = tk.PhotoImage(file=str(CHECKED_ICON_PATH))
        self.icon_unchecked = tk.PhotoImage(file=str(UNCHECKED_ICON_PATH))

        # Also keep the string identifiers for easier comparison
        # Depending on Tk version tree.item(..., "image") may return a tuple or string.
        # We'll always compare against str(self.icon_...)
        self._checked_img_str = str(self.icon_checked)
        self._unchecked_img_str = str(self.icon_unchecked)

        # Save callback
        self.on_row_double_click = on_row_double_click

        # Treeview widget
        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            show="tree headings",
            height=height,
            selectmode="none"
        )
        # internal layout within this frame is pack (safe — this frame is used by parent)
        self.tree.pack(fill="both", expand=True)

        # Configure the image checkbox column (#0)
        self.tree.column("#0", width=40, anchor="center", stretch=False)
        self.tree.heading("#0", text="")
        self.tree.tag_configure("checked", background="#d0f0c0")  # light green

        # Configure remaining columns
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="w")

        # Bind left click for toggling checkbox (image) in the tree column
        self.tree.bind("<Button-1>", self._handle_click)

        # Bind double click if callback provided
        if on_row_double_click:
            self.tree.bind("<Double-1>", self._on_double_click)

    # --------------------------
    # Public API
    # --------------------------
    def insert_row(self, id: Any, values: Iterable[Any]):
        """
        Insert a single row.
        - id: unique identifier (will be converted to str and used as iid)
        - values: iterable containing values in the same order as self.columns
        """
        iid = str(id)
        vals = list(values)
        # Ensure values length matches columns length (pad with empty strings if shorter)
        if len(vals) < len(self.columns):
            vals = vals + [""] * (len(self.columns) - len(vals))
        self.tree.insert("", "end", iid=iid,
                         image=self.icon_unchecked, values=vals)

    def refresh_list(self, rows: Iterable):
        """
        Replace all rows in the tree.
        Accepts rows as:
         - dicts with 'id' and keys matching self.columns
         - sequences where first item is id, rest are column values
        """
        # remove existing items
        for child in self.tree.get_children():
            self.tree.delete(child)

        for row in rows:
            if isinstance(row, dict):
                if "id" not in row:
                    raise ValueError("row dict must contain an 'id' key")
                iid = row["id"]
                # Build values in the correct column order
                values = [row.get(col, "") for col in self.columns]
            else:
                # treat as sequence: first element is id
                seq = list(row)
                if len(seq) == 0:
                    continue
                iid = seq[0]
                values = seq[1:]
            self.insert_row(iid, values)

    def get_checked(self) -> List[str]:
        """Return list of iids (strings) that are currently checked."""
        checked = []
        for iid in self.tree.get_children():
            img_field = self.tree.item(iid, "image")
            img_str = self._image_field_to_str(img_field)
            if img_str == self._checked_img_str:
                checked.append(iid)
        return checked

    def get_selected_row(self) -> Optional[str]:
        """Return the currently focused row iid or None."""
        item = self.tree.focus()
        return item if item else None

    def update_row(self, iid: str, values: Optional[Iterable[Any]] = None, checked: Optional[bool] = None):
        """
        Update a single row by iid.
        - values: list of new column values (must match self.columns length or shorter)
        - checked: True/False to set checkbox, None to leave unchanged
        """
        if iid not in self.tree.get_children():
            raise ValueError(f"No row with iid={iid}")

        # Update values
        if values is not None:
            vals = list(values)
            if len(vals) < len(self.columns):
                vals += [""] * (len(self.columns) - len(vals))
            self.tree.item(iid, values=vals)

        # Update checked state
        if checked is not None:
            if checked:
                self.tree.item(iid, image=self.icon_checked, tags=("checked",))
            else:
                self.tree.item(iid, image=self.icon_unchecked, tags=())

    def update_checked_rows(self, values: Optional[Dict[str, Iterable[Any]]] = None, checked: Optional[bool] = None):
        """
        Update all checked rows.
        - values: dict mapping iid -> list of new column values
        - checked: True/False to set checkbox state
        """
        for iid in self.get_checked():
            row_values = values[iid] if values and iid in values else None
            self.update_row(iid, values=row_values, checked=checked)

    # --------------------------
    # Internal helpers / events
    # --------------------------
    def _on_double_click(self, event):
        iid = self.get_selected_row()
        if iid and self.on_row_double_click:
            try:
                self.on_row_double_click(iid)
            except Exception:
                # swallow to avoid crashing GUI; caller should handle exceptions
                pass

    def _handle_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "tree":
            return

        row = self.tree.identify_row(event.y)
        if not row:
            return

        img_field = self.tree.item(row, "image")
        img_str = self._image_field_to_str(img_field)

        # Toggle checkbox image
        if img_str == self._unchecked_img_str:
            new_image = self.icon_checked
            self.tree.item(row, image=new_image, tags=("checked",))
        else:
            new_image = self.icon_unchecked
            self.tree.item(row, image=new_image, tags=())

    @staticmethod
    def _image_field_to_str(img_field) -> str:
        """
        Normalise the value returned by tree.item(..., "image") to a string identifier.
        Tk may return a tuple like ('pyimage12',) or a string 'pyimage12'.
        """
        if isinstance(img_field, tuple) and len(img_field) > 0:
            return str(img_field[0])
        return str(img_field)
