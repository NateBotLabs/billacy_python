"""Repository for User model, inherits generic CRUD from BaseRepository."""
from app.models.media import Media
from .base import BaseRepository


class MediaRepository(BaseRepository):
    """Repository for Media model, inherits generic CRUD from BaseRepository."""

    def __init__(self):
        super().__init__(Media)
