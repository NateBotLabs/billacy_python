"""Factory for creating Invoice instances for testing."""
import factory
from datetime import datetime, timedelta
from app.models import User
from tests.factories.base_factory import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    first_name = factory.LazyAttribute(
        lambda obj: BaseFactory._fake.first_name())
    last_name = factory.LazyAttribute(
        lambda obj: BaseFactory._fake.last_name())
    email = factory.LazyAttribute(
        lambda obj: BaseFactory._fake.unique.email())
    class_id = None  # Can be set to a specific class ID if needed
