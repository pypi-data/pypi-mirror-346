from typing import ClassVar, List, Optional, Type

from crudclient.exceptions import NotFoundError
from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import (
    VoucherType,
    VoucherTypeResponse,
)

from .ledger import TripletexLedger


class TripletexVoucherType(TripletexCrud[VoucherType]):
    """API methods for interacting with ledger voucher types."""

    _resource_path: ClassVar[str] = "voucherType"
    _datamodel: ClassVar[Type[VoucherType]] = VoucherType
    _api_response_model: ClassVar[Type[VoucherTypeResponse]] = VoucherTypeResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger
    _methods: ClassVar[List[str]] = ["list", "read"]

    def search(
        self, name: Optional[str] = None, from_index: int = 0, count: int = 1000, sorting: Optional[str] = None, fields: Optional[str] = None
    ) -> List[VoucherType]:
        """
        Find voucher types corresponding with sent data.

        Args:
            name: Containing
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of VoucherType objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if name:
            params["name"] = name
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Note: The base list method returns the full response model if _api_response_model is set.
        # To maintain the original return type List[VoucherType], we access .values
        response = self.list(params=params)
        if isinstance(response, self._api_response_model):
            return response.values
        # Fallback in case the response structure changes or isn't the expected model
        return response  # type: ignore

    def find_by_name_or_404(self, name: str) -> VoucherType:
        """
        Retrieve a single voucher type by its exact name.

        Args:
            name: The voucher type name to search for.

        Returns:
            The VoucherType object if found.

        Raises:
            NotFoundError: If exactly one voucher type with the given name is not found.
        """
        # Use search with count=2 to efficiently check if 0, 1, or >1 voucher types exist
        results = self.search(name=name, count=2)

        if len(results) == 1:
            return results[0]
        else:
            raise NotFoundError(f"Expected 1 voucher type with name '{name}', found {len(results)}")
