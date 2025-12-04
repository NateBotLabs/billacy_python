"""User model definition."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class User(Base):
    """User model representing a system user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(200), unique=True, nullable=True)
    class_id = Column(Integer, ForeignKey("student_classes.id"))

    student_class = relationship("StudentClass", back_populates="students")
    invoices = relationship("Invoice", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
