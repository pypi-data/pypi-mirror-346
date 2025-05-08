# Removed: from crudclient.utils import redact_json_body (causes ModuleNotFoundError)
from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.supplier.models import (
    Supplier,
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)


class TripletexSuppliers(TripletexCrud[Supplier]):
    _resource_path = "supplier"
    _datamodel = Supplier
    _create_model = SupplierCreate
    _update_model = SupplierUpdate
    _api_response_model = SupplierResponse
    _list_key = "values"
    allowed_actions = ["list", "read", "create", "update", "destroy"]
