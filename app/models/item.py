from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Item(Base):
    """Invoice item model."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)

    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)

    invoice = relationship("Invoice", back_populates="items")

    def __repr__(self):
        return f"<Item id={self.id} name={self.name} qty={self.quantity} price={self.price}>"
