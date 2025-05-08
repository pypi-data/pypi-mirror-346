from typing import Any, ClassVar, List, Type

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.supplier.models import Supplier, SupplierCreate, SupplierUpdate

class TripletexSuppliers(TripletexCrud[Supplier]):
    """API endpoint for managing suppliers in Tripletex."""

    _resource_path: ClassVar[str]
    _datamodel: ClassVar[Type[Supplier]]
    _create_model: ClassVar[Type[SupplierCreate]]
    _update_model: ClassVar[Type[SupplierUpdate]]
    allowed_actions: ClassVar[List[str]]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the supplier endpoint, configuring the response strategy."""
        ...

    def _dump_data(self, data: Any, partial: bool = False) -> Any:
        """
        Validate and dump data using create/update models if available.

        Overrides the default behavior to use `_create_model` for full updates
        and `_update_model` for partial updates, falling back to the superclass
        method if the specific models are not defined or applicable.

        Args:
            data: The data to validate and dump.
            partial: If True, use the update model and exclude unset fields.
                     If False, use the create model.

        Returns:
            The validated and dumped data suitable for JSON serialization.

        Raises:
            DataValidationError: If validation fails against the chosen model.
        """
        ...
