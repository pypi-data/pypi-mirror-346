# /workspace/tripletex/endpoints/employee/models.pyi
from typing import ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict

from tripletex.core.models import IdUrl, TripletexResponse

class Employee(BaseModel):
    """Represents a Tripletex employee."""

    first_name: Optional[str]
    """Employee's first name."""
    last_name: Optional[str]
    """Employee's last name."""
    id: Optional[int]
    """Unique identifier."""
    version: Optional[int]
    """Version number for optimistic locking."""
    changes: Optional[list[str]]
    """List of changes."""
    url: Optional[str]
    """URL to the employee resource."""
    display_name: Optional[str]
    """Full name for display."""
    employee_number: Optional[str]
    """Employee identification number."""
    date_of_birth: Optional[str]
    """Date of birth (YYYY-MM-DD)."""
    email: Optional[str]
    """Email address."""
    phone_number_mobile_country: Optional[IdUrl]
    """Country code for mobile phone number."""
    phone_number_mobile: Optional[str]
    """Mobile phone number."""
    phone_number_home: Optional[str]
    """Home phone number."""
    phone_number_work: Optional[str]
    """Work phone number."""
    national_identity_number: Optional[str]
    """National identity number."""
    dnumber: Optional[str]
    """D-number (alternative ID)."""
    international_id: Optional[IdUrl]
    """International ID details."""
    bank_account_number: Optional[str]
    """Bank account number."""
    iban: Optional[str]
    """IBAN number."""
    bic: Optional[str]
    """BIC/SWIFT code."""
    creditor_bank_country_id: Optional[int]
    """ID of the creditor bank's country."""
    uses_abroad_payment: Optional[bool]
    """Flag indicating if abroad payments are used."""
    user_type: Optional[IdUrl]
    """Type of user."""
    allow_information_registration: Optional[bool]
    """Flag allowing information registration."""
    is_contact: Optional[bool]
    """Flag indicating if the employee is a contact."""
    is_proxy: Optional[bool]
    """Flag indicating if the employee is a proxy."""
    comments: Optional[str]
    """Additional comments."""
    address: Optional[IdUrl]
    """Link to the employee's address."""
    department: IdUrl
    """Link to the employee's department."""
    employments: Optional[List[IdUrl]]
    """Link to employment details."""
    holiday_allowance_earned: Optional[IdUrl]
    """Link to holiday allowance details."""
    employee_category: Optional[IdUrl]
    """Link to the employee category."""
    is_auth_project_overview_url: Optional[bool]
    """Flag related to project overview authorization."""
    picture_id: Optional[int]
    """ID of the employee's picture."""
    company_id: Optional[int]
    """ID of the associated company."""

    model_config: ClassVar[ConfigDict]
    """Pydantic model configuration."""

class EmployeeCreate(BaseModel):
    """Input model for creating an Employee."""

    first_name: str
    """Employee's first name (required)."""
    last_name: str
    """Employee's last name (required)."""
    email: str
    """Email address (required)."""
    department: IdUrl
    """Link to the employee's department (required)."""
    employee_number: Optional[str]
    """Employee identification number."""
    date_of_birth: Optional[str]
    """Date of birth (YYYY-MM-DD)."""
    phone_number_mobile_country: Optional[IdUrl]
    """Country code for mobile phone number."""
    phone_number_mobile: Optional[str]
    """Mobile phone number."""
    phone_number_home: Optional[str]
    """Home phone number."""
    phone_number_work: Optional[str]
    """Work phone number."""
    national_identity_number: Optional[str]
    """National identity number."""
    dnumber: Optional[str]
    """D-number (alternative ID)."""
    international_id: Optional[IdUrl]
    """International ID details."""
    bank_account_number: Optional[str]
    """Bank account number."""
    iban: Optional[str]
    """IBAN number."""
    bic: Optional[str]
    """BIC/SWIFT code."""
    creditor_bank_country_id: Optional[int]
    """ID of the creditor bank's country."""
    uses_abroad_payment: Optional[bool]
    """Flag indicating if abroad payments are used."""
    user_type: Optional[IdUrl]
    """Type of user."""
    allow_information_registration: Optional[bool]
    """Flag allowing information registration."""
    is_contact: Optional[bool]
    """Flag indicating if the employee is a contact."""
    is_proxy: Optional[bool]
    """Flag indicating if the employee is a proxy."""
    comments: Optional[str]
    """Additional comments."""
    address: Optional[IdUrl]
    """Link to the employee's address."""
    employments: Optional[List[IdUrl]]
    """Link to employment details."""
    holiday_allowance_earned: Optional[IdUrl]
    """Link to holiday allowance details."""
    employee_category: Optional[IdUrl]
    """Link to the employee category."""
    is_auth_project_overview_url: Optional[bool]
    """Flag related to project overview authorization."""
    picture_id: Optional[int]
    """ID of the employee's picture."""

class EmployeeUpdate(BaseModel):
    """Input model for updating an Employee. All fields are optional."""

    first_name: Optional[str]
    """Employee's first name."""
    last_name: Optional[str]
    """Employee's last name."""
    email: Optional[str]
    """Email address."""
    department: Optional[IdUrl]
    """Link to the employee's department."""
    employee_number: Optional[str]
    """Employee identification number."""
    date_of_birth: Optional[str]
    """Date of birth (YYYY-MM-DD)."""
    phone_number_mobile_country: Optional[IdUrl]
    """Country code for mobile phone number."""
    phone_number_mobile: Optional[str]
    """Mobile phone number."""
    phone_number_home: Optional[str]
    """Home phone number."""
    phone_number_work: Optional[str]
    """Work phone number."""
    national_identity_number: Optional[str]
    """National identity number."""
    dnumber: Optional[str]
    """D-number (alternative ID)."""
    international_id: Optional[IdUrl]
    """International ID details."""
    bank_account_number: Optional[str]
    """Bank account number."""
    iban: Optional[str]
    """IBAN number."""
    bic: Optional[str]
    """BIC/SWIFT code."""
    creditor_bank_country_id: Optional[int]
    """ID of the creditor bank's country."""
    uses_abroad_payment: Optional[bool]
    """Flag indicating if abroad payments are used."""
    user_type: Optional[IdUrl]
    """Type of user."""
    allow_information_registration: Optional[bool]
    """Flag allowing information registration."""
    is_contact: Optional[bool]
    """Flag indicating if the employee is a contact."""
    is_proxy: Optional[bool]
    """Flag indicating if the employee is a proxy."""
    comments: Optional[str]
    """Additional comments."""
    address: Optional[IdUrl]
    """Link to the employee's address."""
    employments: Optional[List[IdUrl]]
    """Link to employment details."""
    holiday_allowance_earned: Optional[IdUrl]
    """Link to holiday allowance details."""
    employee_category: Optional[IdUrl]
    """Link to the employee category."""
    is_auth_project_overview_url: Optional[bool]
    """Flag related to project overview authorization."""
    picture_id: Optional[int]
    """ID of the employee's picture."""

class EmployeeResponse(TripletexResponse[Employee]):
    """Response wrapper for a list of Employee objects."""

    pass
