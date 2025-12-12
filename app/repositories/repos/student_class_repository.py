"""Repository for User model, inherits generic CRUD from BaseRepository."""
from app.models.student_class import StudentClass
from .base import BaseRepository


class StudentClassRepository(BaseRepository):
    """Repository for StudentClass model, inherits generic CRUD from BaseRepository."""

    def __init__(self):
        super().__init__(StudentClass)


