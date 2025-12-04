"""Model representing a class for students."""
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.models.base import Base


class StudentClass(Base):
    """Model representing a class for students."""
    __tablename__ = "student_classes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(225), nullable=False)
    description = Column(String(225), default="")
    tutor = Column(String(225), default=None)
    tuition_fee = Column(Float, default=0.0)

    students = relationship("User", back_populates="student_class")
