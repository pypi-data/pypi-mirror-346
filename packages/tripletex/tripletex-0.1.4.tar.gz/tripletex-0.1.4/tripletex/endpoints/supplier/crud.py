from typing import ClassVar, List, Optional, Type

from crudclient.exceptions import NotFoundError
from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.supplier.models import (
    Supplier,
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)


class TripletexSuppliers(TripletexCrud[Supplier]):
    """API endpoint for managing suppliers in Tripletex."""

    _resource_path: ClassVar[str] = "supplier"
    _datamodel: ClassVar[Type[Supplier]] = Supplier
    _create_model: ClassVar[Type[SupplierCreate]] = SupplierCreate
    _update_model: ClassVar[Type[SupplierUpdate]] = SupplierUpdate
    _api_response_model: ClassVar[Type[SupplierResponse]] = SupplierResponse
    _list_key: ClassVar[str] = "values"
    allowed_actions: ClassVar[List[str]] = ["list", "read", "create", "update", "destroy"]

    def search(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        supplier_number: Optional[str] = None,
        organization_number: Optional[str] = None,
        email: Optional[str] = None,
        invoice_email: Optional[str] = None,
        is_inactive: Optional[bool] = None,
        account_manager_id: Optional[str] = None,
        changed_since: Optional[str] = None,
        is_wholesaler: Optional[bool] = None,
        show_products: Optional[bool] = None,
        is_supplier: Optional[bool] = None,
        is_customer: Optional[bool] = None,
        from_index: int = 0,
        count: int = 1000,
        sorting: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> List[Supplier]:
        """
        Find suppliers corresponding with sent data.

        Args:
            id: List of IDs
            name: Supplier name
            supplier_number: Supplier number
            organization_number: Organization number
            email: Email address
            invoice_email: Invoice email address
            is_inactive: Is inactive
            account_manager_id: Account manager ID
            changed_since: Only return elements that have changed since this date and time
            is_wholesaler: Is wholesaler
            show_products: Show products
            is_supplier: Is supplier
            is_customer: Is customer
            from_index: From index
            count: Number of elements to return
            sorting: Sorting pattern
            fields: Fields filter pattern

        Returns:
            List of Supplier objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if id:
            params["id"] = id
        if name:
            params["name"] = name
        if supplier_number:
            params["supplierNumber"] = supplier_number
        if organization_number:
            params["organizationNumber"] = organization_number
        if email:
            params["email"] = email
        if invoice_email:
            params["invoiceEmail"] = invoice_email
        if is_inactive is not None:
            params["isInactive"] = is_inactive
        if account_manager_id:
            params["accountManagerId"] = account_manager_id
        if changed_since:
            params["changedSince"] = changed_since
        if is_wholesaler is not None:
            params["isWholesaler"] = is_wholesaler
        if show_products is not None:
            params["showProducts"] = show_products
        if is_supplier is not None:
            params["isSupplier"] = is_supplier
        if is_customer is not None:
            params["isCustomer"] = is_customer
        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        return self.list(params=params)

    def get_by_name_or_404(self, name: str) -> Supplier:
        """
        Retrieve a single supplier by its name.

        Args:
            name: The supplier name to search for.

        Returns:
            The Supplier object if found.

        Raises:
            NotFoundError: If exactly one supplier with the given name is not found.
        """
        # Use count=2 to efficiently check if 0, 1, or >1 suppliers exist
        response = self.search(name=name, count=2)

        # The response is a SupplierResponse object with a values attribute
        suppliers = response.values if hasattr(response, "values") else []

        if len(suppliers) == 1:
            return suppliers[0]
        else:
            raise NotFoundError(f"Expected 1 supplier with name '{name}', found {len(suppliers)}")

    def get_by_organization_number_or_404(self, organization_number: str) -> Supplier:
        """
        Retrieve a single supplier by its organization number.

        Args:
            organization_number: The organization number to search for.

        Returns:
            The Supplier object if found.

        Raises:
            NotFoundError: If exactly one supplier with the given organization number is not found.
        """
        # Use count=2 to efficiently check if 0, 1, or >1 suppliers exist
        response = self.search(organization_number=organization_number, count=2)

        # The response is a SupplierResponse object with a values attribute
        suppliers = response.values if hasattr(response, "values") else []

        if len(suppliers) == 1:
            return suppliers[0]
        else:
            raise NotFoundError(f"Expected 1 supplier with organization number '{organization_number}', found {len(suppliers)}")
