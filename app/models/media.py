# app/models/media.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base  # assuming your declarative base is here


class Media(Base):
    """Model representing uploaded media files."""
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # profile, document, media
    category = Column(String(50), nullable=False)
    original_filename = Column(String(255), nullable=False)
    storage_filename = Column(String(255), nullable=False, unique=True)
    uploaded_at = Column(DateTime, default=datetime.now())

    # Optional: you could add user_id if you plan to track uploads per user
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
