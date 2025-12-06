"""Repository module for Invoice entity."""
from app.repositories.repos.base import BaseRepository
from app.models.invoice import Invoice


class InvoiceRepository(BaseRepository):
    """Repository for managing Invoice entities in the database."""
    def __init__(self):
        super().__init__(Invoice)
    

    def get_by_user_id(self, user_id):
        """Retrieve all invoices for a specific user."""
        return self.session.query(Invoice).filter(Invoice.user_id == user_id).all()