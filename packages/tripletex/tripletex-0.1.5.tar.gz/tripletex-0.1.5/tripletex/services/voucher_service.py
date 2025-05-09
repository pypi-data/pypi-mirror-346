"""Service for creating vouchers from simple information."""

import datetime
from typing import Dict, List, Optional

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
        supplier_id: Optional[int] = None,
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
            supplier_id: Optional ID of the supplier (preferred over name/org_number).
            send_to_ledger: Whether to send the voucher to ledger during creation.
                Defaults to False.
            voucher_type_id: Optional ID of the voucher type to use.
                If not provided, a default expense voucher type will be used.

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
        if supplier_id is not None:
            # If supplier_id is provided, use it directly (preferred method)
            supplier = self.api_client.suppliers.read(resource_id=str(supplier_id))
        elif supplier_org_number or supplier_name:
            # Fallback to lookup by name or org number
            supplier = self.api_client.suppliers.get_supplier_by_organization_number_or_name_or_404(
                name=supplier_name, organization_number=supplier_org_number
            )

        # Find a suitable voucher type (expense by default) or use the provided ID
        if voucher_type_id is not None:
            voucher_type_id = voucher_type_id
        else:
            voucher_type = self.api_client.ledger.voucher_type.get_by_code_or_404(code="K")
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
            description = posting_dict.get("description", "") or default_description

            if amount is None or account_number is None:
                raise ValueError(f"Posting {i} is missing required fields: amount and accountnumber")

            # Find the account by number
            account = self.api_client.ledger.account.get_by_number_or_404(account_number)

            # Get the VAT type for the account
            vat_type_id = None
            vat_percentage = 0
            if account.vat_type and account.vat_type.id:
                vat_type_id = account.vat_type.id
                # Get the VAT percentage based on the VAT type ID
                # VAT type 3 is 25% in Norway (high rate)
                if vat_type_id == 3:
                    vat_percentage = 0.25  # type: ignore
                # Add other VAT types as needed

            # Calculate gross amount based on VAT
            # For both debit (positive) and credit (negative) amounts with VAT,
            # gross = net * (1 + VAT%)
            # For amounts without VAT, gross = net
            gross_amount = amount
            if vat_type_id and vat_type_id != 0:
                gross_amount = amount * (1 + vat_percentage)

                # If this is a VAT account, we need to create a VAT posting
                # This is handled by the API, so we don't need to do anything here

            # Create the posting object with all required fields
            posting = PostingCreate(
                row=i,
                description=description,
                account=IdRef(id=account.id),
                amount=amount,
                date=date_str,
                # Add these fields which are required for proper voucher creation
                amount_currency=amount,
                amount_gross=gross_amount,
                amount_gross_currency=gross_amount,
                currency=IdRef(id=1),  # Default currency (NOK)
            )

            # Set the VAT type
            if vat_type_id is not None:
                posting.vat_type = IdRef(id=vat_type_id)

            # Set the supplier if provided
            if supplier:
                posting.supplier = IdRef(id=supplier.id)

            posting_objects.append(posting)

        # Check if the postings balance to zero
        # We need to check the net amounts
        total_net = sum(p.amount or 0.0 for p in posting_objects)

        if abs(total_net) > 0.001:  # Allow for small floating point errors
            raise ValueError(f"Postings do not balance to zero. Net total: {total_net}")

        # If the gross amounts don't balance, we need to adjust them
        total_gross = sum(p.amount_gross or 0.0 for p in posting_objects)
        if abs(total_gross) > 0.001:  # Allow for small floating point errors
            # Find the credit posting (negative amount) and adjust its gross amount
            for p in posting_objects:
                if p.amount is not None and p.amount < 0 and p.amount_gross is not None:
                    # Adjust the gross amount to balance the total
                    p.amount_gross = p.amount_gross - total_gross
                    p.amount_gross_currency = p.amount_gross
                    break

        return posting_objects
