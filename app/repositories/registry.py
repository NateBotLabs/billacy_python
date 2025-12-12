# app/repositories/registry.py
from enum import Enum

# Import repositories
from .repos.invoice_repository import InvoiceRepository
from .repos.item_repository import ItemRepository
from .repos.student_class_repository import StudentClassRepository
from .repos.user_repository import UserRepository
from .repos.media_repository import MediaRepository


class RepoName(str, Enum):
    INVOICE = "invoice"
    ITEM = "item"
    STUDENT_CLASS = "student_class"
    USER = "user"
    MEDIA = "media"


# Map symbols to repository classes
REPO_MAP = {
    RepoName.INVOICE: InvoiceRepository,
    RepoName.ITEM: ItemRepository,
    RepoName.STUDENT_CLASS: StudentClassRepository,
    RepoName.USER: UserRepository,
    RepoName.MEDIA: MediaRepository,
}


class RepoRegistry:
    """Singleton-style repository registry: returns the same repo instance for each model."""

    _instances = {}  # Cache of repository instances

    @classmethod
    def get(cls, repo_symbol: RepoName):
        if repo_symbol in cls._instances:
            return cls._instances[repo_symbol]  # Return cached instance

        repo_class = REPO_MAP.get(repo_symbol)
        if not repo_class:
            raise ValueError(f"No repository registered for '{repo_symbol}'")

        instance = repo_class()
        cls._instances[repo_symbol] = instance  # Cache it
        return instance
