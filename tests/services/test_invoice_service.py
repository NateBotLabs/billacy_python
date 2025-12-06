# tests/services/test_invoice_service.py
from tests.base_test import *
from app.services.invoice_service import InvoiceService


class TestInvoiceService(BaseTest):

    def setup_method(self):
        self.service = InvoiceService()  # safe: no factories here

    def test_create_invoice_for_user(self):
        # Factory instance created inside test -> session attached
        user = UserFactory()
        items_data = [
            {"name": "Uniform", "quantity": 2, "price": 10000},
            {"name": "PTA", "quantity": 1, "price": 1000},
        ]

        self.service.create_invoice_for_user(user.id, items_data)

        saved_invoice = RepoRegistry.get(
            RepoName.INVOICE).get_by_user_id(user.id)[0]
        assert saved_invoice is not None
        assert saved_invoice.user_id == user.id
        assert len(saved_invoice.items) == 2

    def test_create_invoice_with_factory(self):
        invoice = InvoiceFactory()
        saved_invoice = RepoRegistry.get(
            RepoName.INVOICE).get_by_id(invoice.id)
        assert saved_invoice is not None
