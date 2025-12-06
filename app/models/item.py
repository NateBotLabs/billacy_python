from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.relations.invoice_item_association import invoice_item_assoc


class Item(Base):
    """Invoice item model."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    deleted = Column(Boolean, default=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    invoices = relationship(
        "Invoice",
        secondary=invoice_item_assoc,
        back_populates="items"
    )

    def __repr__(self):
        return f"<Item id={self.id} name={self.name} qty={self.quantity} price={self.price}>"
