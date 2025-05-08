from typing import ClassVar, List, Optional, Type, cast

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.ledger.models import (
    VoucherOpeningBalance,
    VoucherOpeningBalanceResponse,
)

from .voucher import TripletexVoucher


class TripletexVoucherOpeningBalance(TripletexCrud[VoucherOpeningBalance]):
    """API methods for interacting with opening balance vouchers."""

    _resource_path: ClassVar[str] = "openingBalance"
    _datamodel: ClassVar[Type[VoucherOpeningBalance]] = VoucherOpeningBalance
    _api_response_model: ClassVar[Type[VoucherOpeningBalanceResponse]] = VoucherOpeningBalanceResponse
    _parent_resource: ClassVar[Type[TripletexVoucher]] = TripletexVoucher

    def list(self, parent_id: Optional[str] = None, params: Optional[JSONDict] = None) -> List[VoucherOpeningBalance]:
        """
        List opening balance vouchers.

        Args:
            parent_id: Optional parent ID if this is a nested resource
            params: Optional query parameters. Must include 'dateFrom' and 'dateTo'.

        Returns:
            List of VoucherOpeningBalance objects, or an empty list if no opening balance voucher is found

        Raises:
            UnprocessableEntityError: If dateFrom or dateTo is missing
        """
        if params is None:
            params = {}

        # Ensure required parameters are present
        if "dateFrom" not in params or "dateTo" not in params:
            # Default to current date if not provided
            from datetime import datetime, timedelta

            today = datetime.now().strftime("%Y-%m-%d")
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            if "dateFrom" not in params:
                params["dateFrom"] = yesterday
            if "dateTo" not in params:
                params["dateTo"] = today

        response = super().list(parent_id=parent_id, params=params)

        # Handle the special case for opening balance vouchers
        # The API returns a single object in 'value' field instead of a list in 'values'
        if isinstance(response, VoucherOpeningBalanceResponse):
            if response.value:
                return [response.value]
            return []

        # Fallback case
        return cast(List[VoucherOpeningBalance], response)

    def read(self, resource_id: str, parent_id: Optional[str] = None) -> VoucherOpeningBalance:
        """
        Retrieve a specific opening balance voucher by ID.

        Args:
            resource_id: The ID of the opening balance voucher to retrieve
            parent_id: Optional parent ID if this is a nested resource

        Returns:
            VoucherOpeningBalance object

        Raises:
            NotFoundError: If the opening balance voucher with the given ID does not exist
        """
        response = super().read(resource_id=resource_id, parent_id=parent_id)

        # Handle the special case for opening balance vouchers
        if isinstance(response, VoucherOpeningBalanceResponse):
            if response.value:
                return response.value
            raise ValueError("Unexpected empty response from API")

        # Fallback case
        return cast(VoucherOpeningBalance, response)

    def search(
        self,
        number: Optional[str] = None,
        number_from: Optional[int] = None,
        number_to: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[VoucherOpeningBalance]:
        """
        Find opening balance vouchers corresponding with sent data.

        Args:
            number: Voucher number
            number_from: From voucher number
            number_to: To voucher number
            date_from: From and including date (format YYYY-MM-DD). Required.
            date_to: To and including date (format YYYY-MM-DD). Required.
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of VoucherOpeningBalance objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if number:
            params["number"] = number
        if number_from:
            params["numberFrom"] = number_from
        if number_to:
            params["numberTo"] = number_to

        # Handle date parameters - required by the API
        from datetime import datetime, timedelta

        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        params["dateFrom"] = date_from if date_from else yesterday
        params["dateTo"] = date_to if date_to else today

        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)
