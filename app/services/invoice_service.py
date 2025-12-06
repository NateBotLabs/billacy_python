# app/services/invoice_service.py
from app.repositories.registry import RepoRegistry, RepoName
from app.models.invoice import Invoice
from app.models.item import Item


class InvoiceService:
    """Service layer for managing invoices."""

    def __init__(self):
        return

    def create_invoice_for_user(self, user_id, items_data, due_date=None):
        """Create an invoice for a user with given items."""
        RepoRegistry(RepoName.ITEM).bulk_insert(items_data)
        item_objs = [Item(**i) for i in items_data]
        invoice = Invoice(user_id=user_id, items=item_objs, due_date=due_date)
        invoice.items = item_objs
        RepoRegistry(RepoName.INVOICE).insert(invoice)

        return invoice

    def get_all_invoices(self):
        """Get all invoices."""
        return RepoRegistry(RepoName.INVOICE).get_all()

    def get_invoices_for_user(self, user_id):
        """Get all invoices for a specific user."""
        return [inv for inv in RepoRegistry(RepoName.INVOICE).get_by_user_id(user_id)]
