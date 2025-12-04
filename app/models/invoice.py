from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class Invoice(Base):
    """Invoice model representing a billing invoice."""

    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_paid = Column(Boolean, default=False)
    total_amount = Column(Float, nullable=False, default=0)
    invoice_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))

    user = relationship("User", back_populates="invoices")
    items = relationship("Item", back_populates="invoice", cascade="all, delete-orphan")

    def recalc_total(self):
        """Recalculate total from items"""
        self.total_amount = sum(item.price * item.quantity for item in self.items)

    def __repr__(self):
        return f"<Invoice id={self.id} user={self.user_id} total={self.total_amount}>"
