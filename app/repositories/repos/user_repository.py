"""Repository for User model, inherits generic CRUD from BaseRepository."""
from app.models.user import User
from .base import BaseRepository


class UserRepository(BaseRepository):
    """Repository for User model, inherits generic CRUD from BaseRepository."""
    def __init__(self):
        super().__init__(User)
