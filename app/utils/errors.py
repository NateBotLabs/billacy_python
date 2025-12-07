""""Custom error classes for operations.
"""


class DatabaseNotInitializedError(RuntimeError):
    """Raised when the database session is accessed before initialization."""


class UnknownEnvironmentError(RuntimeError):
    """Raised when an unknown environment is specified."""


class RecordNotFoundError(LookupError):
    """Raised when a database record is not found."""


class UnexpectedError(Exception):
    """Raised for unexpected errors in the application."""


class LoginIssueError(Exception):
    """Raised for login issue errors"""
