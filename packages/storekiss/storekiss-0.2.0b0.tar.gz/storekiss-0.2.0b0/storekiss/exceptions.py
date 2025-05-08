"""
Custom exceptions for the storekiss library.
"""


class HellodevinError(Exception):
    """Base exception for all storekiss errors."""
    pass


class ValidationError(HellodevinError):
    """Raised when data validation fails."""
    pass


class NotFoundError(HellodevinError):
    """Raised when a requested item is not found."""
    pass


class DatabaseError(HellodevinError):
    """Raised when there's an error with the database operations."""
    pass
