from typing import ClassVar, List, Optional, Type

from crudclient.types import JSONDict

from tripletex.core.crud import TripletexCrud
from tripletex.core.models import IdRef
from tripletex.endpoints.ledger.crud.posting import TripletexPosting
from tripletex.endpoints.ledger.models.posting import PostingCreate

# Import base models used by the class definition directly from voucher.py
from tripletex.endpoints.ledger.models.voucher import (
    Voucher,
    VoucherCreate,
    VoucherResponse,
    VoucherUpdate,
)
from tripletex.utils import ensure_date_params

from .ledger import TripletexLedger


class TripletexVoucher(TripletexCrud[Voucher]):
    """API methods for interacting with ledger vouchers."""

    _resource_path: ClassVar[str] = "voucher"
    _datamodel: ClassVar[Type[Voucher]] = Voucher
    _create_model: ClassVar[Type[VoucherCreate]] = VoucherCreate
    _update_model: ClassVar[Type[VoucherUpdate]] = VoucherUpdate
    _api_response_model: ClassVar[Type[VoucherResponse]] = VoucherResponse
    _parent_resource: ClassVar[Type[TripletexLedger]] = TripletexLedger

    def list(self, parent_id: Optional[str] = None, params: Optional[JSONDict] = None):
        """
        List vouchers.

        Args:
            parent_id: Optional parent ID if this is a nested resource
            params: Optional query parameters. Must include 'dateFrom' and 'dateTo'.

        Returns:
            VoucherResponse object containing a list of Voucher objects

        Raises:
            UnprocessableEntityError: If dateFrom or dateTo is missing
        """

        # Ensure required date parameters are present, defaulting if necessary
        params = ensure_date_params(params)

        return super().list(parent_id=parent_id, params=params)

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
    ):
        """
        Find vouchers corresponding with sent data.

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
            List of Voucher objects
        """
        params: JSONDict = {"from": from_index, "count": count}

        if number:
            params["number"] = number
        if number_from:
            params["numberFrom"] = number_from
        if number_to:
            params["numberTo"] = number_to

        # Handle date parameters - required by the API
        # If date_from or date_to are provided, use them; otherwise, use defaults
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to

        params = ensure_date_params(params)

        if sorting:
            params["sorting"] = sorting
        if fields:
            params["fields"] = fields

        # Call the custom action endpoint
        endpoint = self._get_endpoint("search")
        raw_response = self.client.get(endpoint, params=params)

        # Convert the response to a VoucherResponse object
        return self._api_response_model.model_validate(raw_response)

    def get_options(self, voucher_id: str):
        """
        Get meta information about operations available for this voucher (e.g., if deletable).
        GET /ledger/voucher/{id}/options
        Returns a dict, not a Voucher model.
        """
        # Bypass model conversion for this subresource
        endpoint = self._get_endpoint(str(voucher_id), "options")
        return self.client.get(endpoint)

    def get_pdf(self, voucher_id: str):
        """
        Get PDF representation of voucher by ID.
        GET /ledger/voucher/{voucherId}/pdf

        Returns the raw HTTP response object for full header/content access.
        """
        endpoint = self._get_endpoint(str(voucher_id), "pdf")
        response = self.client.http_client.request_raw("GET", endpoint)
        return response

    def list_non_posted(self, params: Optional[JSONDict] = None):
        """
        Find non-posted vouchers.
        GET /ledger/voucher/>nonPosted
        Returns a list of non-posted vouchers.
        """
        # The >nonPosted endpoint returns a response that already has the structure we need
        # We just need to use the client directly to get the raw response
        endpoint = self._get_endpoint(">nonPosted")
        raw_response = self.client.get(endpoint, params=params)
        return self._api_response_model.model_validate(raw_response)

    def download_pdf(self, voucher_id: str, file_path: Optional[str] = None):
        """
        Download PDF for voucher by ID and save to file_path.
        Returns the file path and filename.
        """
        import re

        response = self.get_pdf(voucher_id)
        content_disposition = response.headers.get("Content-Disposition", "")
        filename = "voucher.pdf"
        match = re.search(r'filename="?([^";]+)"?', content_disposition)
        if match:
            filename = match.group(1)
        pdf_bytes = response.content
        if file_path is None:
            file_path = filename
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
        return file_path, filename

    def upload_attachment(self, voucher_id: int, file_path: str):
        """
        Upload an attachment to a voucher.

        Args:
            voucher_id: The ID of the voucher to attach the file to.
            file_path: Path to the file to upload.

        Returns:
            Voucher: The updated voucher object with the attachment.

        Raises:
            ValueError: If the file is not a PDF. The Tripletex API only supports
                       PDF files for voucher attachments. This is an intentional
                       limitation of the API, not a restriction imposed by this client.
        """
        import os

        endpoint = self._get_endpoint(str(voucher_id), "attachment")
        url = self.client.base_url.rstrip("/") + "/" + endpoint.lstrip("/")
        with open(file_path, "rb") as f:
            filename = os.path.basename(file_path)
            # IMPORTANT: The Tripletex API only accepts PDF files for voucher attachments.
            # This is an API limitation, not a client restriction.
            if not filename.lower().endswith(".pdf"):
                raise ValueError("Only PDF files are allowed for voucher attachments. This is a limitation of the Tripletex API.")
            files = {"file": (filename, f, "application/pdf")}
            # Use the requests session directly for multipart upload
            response = self.client.session.post(url, files=files)
            response.raise_for_status()
            data = response.json()
        # Parse as Voucher (wrapped in "value")
        return self._datamodel.model_validate(data["value"])

    def simple_create(
        self,
        description: str,
        date: str,
        debit_account_id: str,
        credit_account_id: str,
        amount: float,
        entity_type: str,
        entity_id: int,
        voucher_type_id: int,
        debit_vat_id: Optional[int] = None,
        credit_vat_id: Optional[int] = None,
    ) -> Voucher:
        """
        Create a simple voucher with one debit and one credit posting.

        Args:
            description: Description of the voucher.
            date: Date of the voucher (format YYYY-MM-DD).
            debit_account_id: Account ID for the debit posting.
            credit_account_id: Account ID for the credit posting.
            amount: Amount for the voucher.
            entity_type: Type of entity ('customer' or 'supplier').
            entity_id: ID of the entity (customer or supplier).
            voucher_type_id: ID of the voucher type to use.
            debit_vat_id: Optional VAT type ID for the debit posting.
            credit_vat_id: Optional VAT type ID for the credit posting.
        Returns:
            Voucher: The created voucher object.
        """
        # Create the first posting
        posting1: PostingCreate = TripletexPosting.create_entity_posting(
            row=1, description=description, account_id=debit_account_id, amount=amount, entity_type=entity_type, entity_id=entity_id
        )

        # Set VAT type for debit posting if provided
        if debit_vat_id is not None:
            posting1.vat_type = IdRef(id=debit_vat_id)

        # Create the second posting
        posting2: PostingCreate = posting1.model_copy(deep=True)
        posting2.row = 2
        posting2.account = IdRef(id=credit_account_id)
        posting2.amount = -amount

        # Set VAT type for credit posting if provided
        if credit_vat_id is not None:
            posting2.vat_type = IdRef(id=credit_vat_id)

        postings: List[PostingCreate] = [posting1, posting2]

        voucher = VoucherCreate(
            description=description,
            date=date,
            postings=postings,
            voucher_type=IdRef(id=voucher_type_id),
        )

        # Call the create method to save the voucher
        return self.create(voucher)
