"""Factory for creating Invoice instances for testing."""
import factory
import random
from datetime import datetime, timedelta
from app.models import StudentClass
from tests.factories.base_factory import BaseFactory


class StudentClassFactory(BaseFactory):
    class Meta:
        model = StudentClass

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(lambda _: BaseFactory._fake.word())
    tuition_fee = factory.LazyAttribute(
        lambda _: round(random.uniform(5, 100), 2))
    tutor = factory.LazyAttribute(lambda _: BaseFactory._fake.name())
