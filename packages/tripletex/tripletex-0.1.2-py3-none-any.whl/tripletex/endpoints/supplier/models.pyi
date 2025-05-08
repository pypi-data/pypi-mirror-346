# tripletex/endpoints/supplier/models.pyi
from typing import Any, Optional

from pydantic import BaseModel

from tripletex.core.models import IdUrl, TripletexResponse

class Supplier(BaseModel):
    """Represents a supplier in Tripletex."""

    name: str
    id: int
    version: int
    changes: Optional[list[str]]
    url: str
    organization_number: Optional[str]
    supplier_number: int
    customer_number: int
    is_supplier: bool
    is_customer: bool
    is_inactive: bool
    email: Optional[str]
    bank_accounts: Optional[list[str]]
    invoice_email: Optional[str]
    overdue_notice_email: Optional[str]
    phone_number: Optional[str]
    phone_number_mobile: Optional[str]
    description: Optional[str]
    is_private_individual: bool
    show_products: bool
    account_manager: Optional[IdUrl]
    postal_address: Optional[IdUrl]
    physical_address: Optional[IdUrl]
    delivery_address: Optional[IdUrl]
    category1: Optional[Any]
    category2: Optional[Any]
    category3: Optional[Any]
    bank_account_presentation: Optional[list[str]]
    currency: IdUrl
    ledger_account: Optional[IdUrl]
    language: str
    is_wholesaler: bool
    display_name: str
    locale: str
    website: str

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class SupplierCreate(BaseModel):
    """Data model for creating a new supplier."""

    name: str
    email: Optional[str]

class SupplierUpdate(BaseModel):
    """Data model for updating an existing supplier."""

    name: Optional[str]
    email: Optional[str]

class SupplierResponse(TripletexResponse[Supplier]):
    """Response wrapper for supplier data."""

    pass
