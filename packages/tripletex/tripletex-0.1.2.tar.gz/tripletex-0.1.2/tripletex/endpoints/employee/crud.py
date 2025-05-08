from typing import List, Type

from tripletex.core.crud import TripletexCrud

from .models import Employee, EmployeeCreate, EmployeeUpdate


class TripletexEmployees(TripletexCrud[Employee]):
    _resource_path: str = "/employee"
    _datamodel: Type[Employee] = Employee
    _create_model: Type[EmployeeCreate] = EmployeeCreate
    _update_model: Type[EmployeeUpdate] = EmployeeUpdate
    allowed_actions: List[str] = ["list", "read", "create", "update"]
    _list_return_keys: List[str] = ["values"]
