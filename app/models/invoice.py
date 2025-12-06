"""Invoice model definition."""
from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app.utils.helpers import InvoiceStatus
from app.models.base import Base
from app.models.relations.invoice_item_association import invoice_item_assoc


class Invoice(Base):
    """Invoice model representing a billing invoice."""

    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_paid = Column(Boolean, default=False)
    total_amount = Column(Float, nullable=False, default=0)
    invoice_date = Column(DateTime, default=datetime.now(timezone.utc))
    due_date = Column(DateTime, default=lambda: datetime.now(
        timezone.utc) + timedelta(days=30))
    status = Column(Enum(InvoiceStatus),
                    default=InvoiceStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))

    user = relationship("User", back_populates="invoices")
    items = relationship(
        "Item",
        secondary=invoice_item_assoc,  # points to the association table
        back_populates="invoices"
    )

    def recalc_total(self):
        """Recalculate total from items"""
        self.total_amount = sum(
            item.price * item.quantity for item in self.items)

    def __repr__(self):
        return f"<Invoice id={self.id} user={self.user_id} total={self.total_amount}>"
