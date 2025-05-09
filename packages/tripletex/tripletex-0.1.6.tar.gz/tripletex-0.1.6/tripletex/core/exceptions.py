"""Custom exceptions for the Tripletex client."""

from crudclient.exceptions import NotFoundError as NotFoundError


class MultipleResourcesFoundError(NotFoundError):
    """Raised when a search expecting one result finds multiple.

    This exception inherits from NotFoundError to maintain compatibility
    with error handling that catches NotFoundError.
    """
