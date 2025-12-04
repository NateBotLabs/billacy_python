"""Repository module for Item entity."""
from app.repositories.base import BaseRepository
from app.models.item import Item

class ItemRepository(BaseRepository):
    """Repository for managing Item entities in the database."""
    def __init__(self):
        super().__init__(Item)