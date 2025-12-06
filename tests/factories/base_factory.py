# factories/base_factory.py
from faker import Faker
import factory


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base factory for all SQLAlchemy models."""
    _fake = Faker()

    _session = None  # Class-level session to be shared across subclasses

    class Meta:
        abstract = True
        sqlalchemy_session = None  # Will be set dynamically per test
        sqlalchemy_session_persistence = "flush"

    @classmethod
    def set_session(cls, session):
        """Set session for this factory and all subclasses."""
        cls._session = session
        cls._meta.sqlalchemy_session = session
        for subclass in cls.__subclasses__():
            subclass.set_session(session)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = cls._meta.sqlalchemy_session or kwargs.pop("_session", None)
        if session is None:
            raise RuntimeError(
                f"No SQLAlchemy session provided for {cls.__name__}!")
        obj = super()._create(model_class, *args, **kwargs)
        session.flush()
        return obj
