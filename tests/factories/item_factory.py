"""Factory for creating Invoice instances for testing."""
import factory
from datetime import datetime, timedelta, timezone
import random
from app.models import Item
from tests.factories.base_factory import BaseFactory

school_items = [
    "Math Textbook", "English Textbook", "Science Lab Kit",
    "Art Supplies", "Pencil Set", "Notebook", "School Bag",
    "Uniform", "Sports Fee", "Library Fee", "Music Class",
    "Field Trip Fee", "Computer Lab Access"
]

class ItemFactory(BaseFactory):
    class Meta:
        model = Item

    id = factory.Sequence(lambda n: n + 1)
    # name= random.choice(school_items)
    name = factory.LazyAttribute(lambda _: BaseFactory._fake.word())
    quantity = factory.LazyAttribute(lambda _: random.randint(1, 5))
    price = factory.LazyAttribute(lambda _: round(random.uniform(5, 100), 2))
