from typing import ClassVar, List, Optional, Type, cast

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import PaymentTypeOut, PaymentTypeOutResponse

from .ledger import TripletexLedger


class TripletexPaymentTypeOut(TripletexCrud[PaymentTypeOut]):
    """API methods for interacting with ledger payment types out."""

    _resource_path: ClassVar[str] = "paymentTypeOut"
    _datamodel: ClassVar[Type[PaymentTypeOut]] = PaymentTypeOut
    _api_response_model: ClassVar[Type[PaymentTypeOutResponse]] = PaymentTypeOutResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger
    _methods: ClassVar[List[str]] = ["list", "read"]

    def list(self, parent_id: Optional[str] = None, params: Optional[JSONDict] = None) -> List[PaymentTypeOut]:
        """
        List payment types out.

        Args:
            parent_id: Optional parent ID if this is a nested resource
            params: Optional query parameters

        Returns:
            List of PaymentTypeOut objects
        """
        response = super().list(parent_id=parent_id, params=params)
        if isinstance(response, PaymentTypeOutResponse):
            return response.values if response.values else []
        return cast(List[PaymentTypeOut], response)

    def search(
        self, name: Optional[str] = None, from_index: int = 0, count: int = 1000, sorting: Optional[str] = None, fields: Optional[str] = None
    ) -> List[PaymentTypeOut]:
        """
        Find payment types out corresponding with sent data.

        Args:
            name: Containing
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of PaymentTypeOut objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if name:
            params["name"] = name
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)
