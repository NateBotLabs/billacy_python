from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base

invoice_item_assoc = Table(
    "invoice_item_assoc",
    Base.metadata,
    Column("invoice_id", Integer, ForeignKey("invoices.id"), primary_key=True),
    Column("item_id", Integer, ForeignKey("items.id"), primary_key=True),
)
