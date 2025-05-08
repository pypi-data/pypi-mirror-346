"""Stub file for the Tripletex Department API endpoint."""

from typing import Any, ClassVar, List, Type

from tripletex.core.crud import TripletexCrud

from .models import Department, DepartmentCreate, DepartmentUpdate

class TripletexDepartments(TripletexCrud[Department]):
    """
    API endpoint for managing departments in Tripletex.

    Provides standard CRUD operations (list, read, create, update, destroy)
    for departments, inheriting base functionality from TripletexCrud.
    """

    _resource_path: ClassVar[str]
    _datamodel: ClassVar[Type[Department]]
    _create_model: ClassVar[Type[DepartmentCreate]]
    _update_model: ClassVar[Type[DepartmentUpdate]]
    allowed_actions: ClassVar[List[str]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the department endpoint, configuring the response strategy."""
        ...
