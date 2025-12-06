"""Factory for creating Invoice instances for testing."""
import random
import factory
from factory import post_generation
from app.models import Invoice
from app.utils.helpers import InvoiceStatus
from tests.factories.base_factory import BaseFactory
from tests.factories.user_factory import UserFactory
from tests.factories.item_factory import ItemFactory
from datetime import datetime, timedelta, timezone


class InvoiceFactory(BaseFactory):
    class Meta:
        model = Invoice

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    status = factory.LazyAttribute(lambda _: BaseFactory._fake.random_element(
        elements=[InvoiceStatus.PENDING, InvoiceStatus.PAID, InvoiceStatus.OVERDUE]))
    due_date = factory.LazyFunction(
        lambda: datetime.now(timezone.utc) + timedelta(days=30))
    created_at = factory.LazyAttribute(lambda _: datetime.now(timezone.utc))
    updated_at = factory.LazyAttribute(lambda _: datetime.now(timezone.utc))
    is_paid = False

    @post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing
            return
        if extracted:
            # If items are passed explicitly
            for item in extracted:
                self.items.append(item)
        else:
            # Otherwise, create a random number of items (0–8)
            for _ in range(random.randint(0, 8)):
                item = ItemFactory()
                self.items.append(item)
