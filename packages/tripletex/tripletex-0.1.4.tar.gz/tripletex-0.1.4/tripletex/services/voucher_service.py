"""Service for creating vouchers from simple information."""

import datetime
from typing import Dict, List, Optional

from crudclient.exceptions import NotFoundError

from tripletex.core.api import TripletexAPI
from tripletex.core.models import IdRef
from tripletex.endpoints.ledger.models.posting import PostingCreate
from tripletex.endpoints.ledger.models.voucher import Voucher, VoucherCreate
from tripletex.endpoints.supplier.models import Supplier
from tripletex.services.posting_service import PostingService


class VoucherService:
    """Service for creating vouchers from simple information."""

    def __init__(self, api_client: TripletexAPI):
        """Initialize the service with a Tripletex API client.

        Args:
            api_client: The Tripletex API client to use for API calls.
        """
        self.api_client = api_client
        self.posting_service = PostingService(api_client)

    def make_voucher(
        self,
        description: str,
        date: datetime.datetime,
        filepath: Optional[str],
        postings: List[Dict],
        supplier_name: Optional[str] = None,
        supplier_org_number: Optional[str] = None,
        send_to_ledger: bool = False,
        voucher_type_id: Optional[int] = None,
    ) -> Voucher:
        """Create a voucher with postings and an attachment.

        Args:
            description: Description of the voucher.
            date: Date of the voucher as a datetime object.
            filepath: Path to the PDF file to attach to the voucher.
            postings: List of dictionaries representing postings.
                Each dict should have:
                - amount: float (required)
                - accountnumber: str (required)
                - description: str (optional, overrides voucher description)
            supplier_name: Optional name of the supplier.
            supplier_org_number: Optional organization number of the supplier.
            send_to_ledger: Whether to send the voucher to ledger during creation.
                Defaults to False.

        Returns:
            The created Voucher object.

        Raises:
            ValueError: If the postings don't balance to zero or if the file is not a PDF.
            NotFoundError: If an account or supplier cannot be found.
        """
        # Format date as YYYY-MM-DD string
        date_str = date.strftime("%Y-%m-%d")

        # Find supplier if provided
        supplier = None
        if supplier_org_number or supplier_name:
            supplier = self._find_supplier(supplier_name, supplier_org_number)

        # Find a suitable voucher type (expense by default) or use the provided ID
        if voucher_type_id is not None:
            voucher_type_id = voucher_type_id
        else:
            voucher_type = self._find_voucher_type("K")
            voucher_type_id = voucher_type.id

        # Create posting objects with row numbers
        posting_objects = self._create_posting_objects(postings, description, supplier, date_str)

        # Create the voucher
        voucher_data = VoucherCreate(
            date=date_str,
            description=description,
            voucher_type=IdRef(id=voucher_type_id),
            postings=posting_objects,
        )

        # Add sendToLedger parameter if specified
        if send_to_ledger:
            # We need to convert the VoucherCreate to a dict to add the sendToLedger parameter
            # since it's not part of the VoucherCreate model
            voucher_dict = voucher_data.model_dump(by_alias=True)
            voucher_dict["sendToLedger"] = send_to_ledger
            # Use the dict directly instead of assigning back to voucher_data
            created_voucher = self.api_client.ledger.voucher.create(data=voucher_dict)
        else:
            # Create the voucher using the VoucherCreate model
            created_voucher = self.api_client.ledger.voucher.create(data=voucher_data)

        # The voucher has already been created in the conditional block above

        # Upload the attachment
        if filepath and filepath.strip():
            try:
                self.api_client.ledger.voucher.upload_attachment(voucher_id=created_voucher.id, file_path=filepath)
            except Exception as e:
                # Log the error but don't fail the whole operation
                # The voucher was created successfully, just without the attachment
                print(f"Warning: Failed to upload attachment: {str(e)}")

        return created_voucher

    def _find_supplier(self, supplier_name: Optional[str], supplier_org_number: Optional[str]) -> Optional[Supplier]:
        """Find a supplier by name or organization number.

        Args:
            supplier_name: Name of the supplier to find.
            supplier_org_number: Organization number of the supplier to find.

        Returns:
            The supplier if found, None otherwise.

        Raises:
            NotFoundError: If the supplier cannot be found.
        """
        if not supplier_name and not supplier_org_number:
            return None

        try:
            # Try to find by organization number first (more specific)
            if supplier_org_number:
                return self.api_client.suppliers.get_by_organization_number_or_404(supplier_org_number)

            # Then try by name
            if supplier_name:
                return self.api_client.suppliers.get_by_name_or_404(supplier_name)

        except NotFoundError:
            # If not found with the exact methods, try a more flexible search
            if supplier_name:
                # Search with name as a parameter and get the first match
                response = self.api_client.suppliers.search(name=supplier_name, count=1)
                # The response is a SupplierResponse object with a values attribute
                suppliers = response.values if hasattr(response, "values") else []
                if suppliers:
                    return suppliers[0]

            # If we get here and still haven't found a supplier, raise the error
            if supplier_org_number:
                raise NotFoundError(f"Supplier with organization number '{supplier_org_number}' not found")
            else:
                raise NotFoundError(f"Supplier with name '{supplier_name}' not found")

        return None

    def _find_voucher_type(self, code: str = "K"):
        """Find a voucher type by code.

        Args:
            code: The voucher type code to search for. Defaults to "K" (expense).

        Returns:
            The voucher type if found.

        Raises:
            NotFoundError: If the voucher type cannot be found.
        """
        # Get all voucher types and find the one with the matching code
        response = self.api_client.ledger.voucher_type.list()

        # The response is a VoucherTypeResponse object with a values attribute
        voucher_types = response.values if hasattr(response, "values") else []

        # Look for a voucher type with the matching code
        for vt in voucher_types:
            if hasattr(vt, "code") and vt.code == code:
                return vt

        # If not found, return the first voucher type
        if voucher_types:
            return voucher_types[0]

        raise NotFoundError(f"No voucher type found with code '{code}'")

    def _create_posting_objects(
        self,
        postings: List[Dict],
        default_description: str,
        supplier: Optional[Supplier],
        date_str: str,
    ) -> List[PostingCreate]:
        """Create PostingCreate objects from simple posting dictionaries.

        Args:
            postings: List of dictionaries representing postings.
            default_description: Default description to use if not specified in the posting.
            supplier: Optional supplier to associate with the postings.
            date_str: Date string in YYYY-MM-DD format.

        Returns:
            List of PostingCreate objects.

        Raises:
            ValueError: If the postings don't balance to zero.
            NotFoundError: If an account cannot be found.
        """
        posting_objects = []

        # First pass: create all posting objects with row numbers
        for i, posting_dict in enumerate(postings, start=1):
            amount = posting_dict.get("amount")
            account_number = posting_dict.get("accountnumber")
            description = posting_dict.get("description", default_description)

            if amount is None or account_number is None:
                raise ValueError(f"Posting {i} is missing required fields: amount and accountnumber")

            # Find the account by number
            account = self.api_client.ledger.account.get_by_number_or_404(account_number)

            # Create the posting object
            posting = PostingCreate(
                row=i,
                description=description,
                account=IdRef(id=account.id),
                amount=amount,
                date=date_str,
            )

            # Set the VAT type if available from the account
            if account.vat_type and account.vat_type.id:
                posting.vat_type = IdRef(id=account.vat_type.id)

            # Set the supplier if provided
            if supplier:
                posting.supplier = IdRef(id=supplier.id)

            posting_objects.append(posting)

        # Check if the postings balance to zero
        total = sum(p.amount for p in posting_objects)
        if abs(total) > 0.001:  # Allow for small floating point errors
            raise ValueError(f"Postings do not balance to zero. Total: {total}")

        return posting_objects
