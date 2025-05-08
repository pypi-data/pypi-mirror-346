from tripletex.core.crud import TripletexCrud

from .models import Department, DepartmentCreate, DepartmentResponse, DepartmentUpdate


class TripletexDepartments(TripletexCrud[Department]):
    _resource_path = "department"
    _datamodel = Department
    _create_model = DepartmentCreate
    _update_model = DepartmentUpdate
    _api_response_model = DepartmentResponse
    allowed_actions = ["list", "read", "create", "update", "destroy"]
