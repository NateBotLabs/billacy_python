# tests/base_test.py
import pytest
from tests.factories import *
from app.repositories.registry import RepoRegistry, RepoName


@pytest.mark.usefixtures("_inject_session")
class BaseTest:
    """All tests inheriting this base share db_session and factories."""

    @pytest.fixture
    def _inject_session(self, db_session):
        """Provide db_session to test and all factories."""
        self.db_session = db_session
        BaseFactory.set_session(db_session)
