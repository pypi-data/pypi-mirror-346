from typing import ClassVar, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import (
    CloseGroup,
    CloseGroupResponse,
)

from .ledger import TripletexLedger


class TripletexCloseGroup(TripletexCrud[CloseGroup]):
    """API methods for interacting with ledger close groups."""

    _resource_path: ClassVar[str] = "closeGroup"
    _datamodel: ClassVar[Type[CloseGroup]] = CloseGroup
    _api_response_model: ClassVar[Type[CloseGroupResponse]] = CloseGroupResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger
    _methods: ClassVar[List[str]] = ["list", "read"]

    def search(
        self,
        date_from: str,
        date_to: str,
        id: Optional[str] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[CloseGroup]:
        """
        Find close groups corresponding with sent data.

        Args:
            date_from: From and including
            date_to: To and excluding
            id: List of IDs
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of CloseGroup objects
        """
        params: JSONDict = {"dateFrom": date_from, "dateTo": date_to, "from": from_index, "count": count}

        if id:
            params["id"] = id
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)
