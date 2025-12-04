# app/services/invoice_service.py
from app.repositories.invoice_repository import InvoiceRepository
from app.repositories.item_repository import ItemRepository
from app.models.invoice import Invoice
from app.models.item import Item


class InvoiceService:
    def __init__(self):
        self.invoice_repo = InvoiceRepository()
        self.item_repo = ItemRepository()

    def create_invoice_for_user(self, user_id, items_data, due_date=None):
        invoice = Invoice(user_id=user_id, items=items_data, due_date=due_date)
        self.invoice_repo.insert(invoice)

        item_objs = [
            Item(name=i['name'], quantity=i['quantity'],
                 price=i['price'], invoice_id=invoice.id)
            for i in items_data
        ]
        self.item_repo.bulk_insert(item_objs)
        return invoice

    def get_all_invoices(self):
        return self.invoice_repo.get_all()

    def get_invoices_for_user(self, user_id):
        return [inv for inv in self.invoice_repo.get_by_user_id(user_id)]
