"""API wrapper for the Tripletex employee endpoint."""

from typing import List, Type

from tripletex.core.crud import TripletexCrud

from .models import Employee, EmployeeCreate, EmployeeUpdate

class TripletexEmployees(TripletexCrud[Employee]):
    """Handles CRUD operations for Tripletex employees."""

    _resource_path: str
    _datamodel: Type[Employee]
    _create_model: Type[EmployeeCreate]
    _update_model: Type[EmployeeUpdate]
    allowed_actions: List[str]
    _list_return_keys: List[str]
