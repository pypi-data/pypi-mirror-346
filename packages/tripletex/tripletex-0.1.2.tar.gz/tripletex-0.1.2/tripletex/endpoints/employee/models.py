# /workspace/tripletex/endpoints/employee/models.py
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import IdUrl, TripletexResponse


class Employee(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id: Optional[int] = None
    version: Optional[int] = None
    changes: Optional[list[str]] = None
    url: Optional[str] = None
    display_name: Optional[str] = None
    employee_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    email: Optional[str] = None
    phone_number_mobile_country: Optional[IdUrl] = None
    phone_number_mobile: Optional[str] = None
    phone_number_home: Optional[str] = None
    phone_number_work: Optional[str] = None
    national_identity_number: Optional[str] = None
    dnumber: Optional[str] = None
    international_id: Optional[IdUrl] = None
    bank_account_number: Optional[str] = None
    iban: Optional[str] = None
    bic: Optional[str] = None
    creditor_bank_country_id: Optional[int] = None
    uses_abroad_payment: Optional[bool] = None
    user_type: Optional[IdUrl] = None
    allow_information_registration: Optional[bool] = None
    is_contact: Optional[bool] = None
    is_proxy: Optional[bool] = None
    comments: Optional[str] = None
    address: Optional[IdUrl] = None
    department: IdUrl
    employments: Optional[List[IdUrl]] = None
    holiday_allowance_earned: Optional[IdUrl] = None
    employee_category: Optional[IdUrl] = None
    is_auth_project_overview_url: Optional[bool] = None
    picture_id: Optional[int] = None
    company_id: Optional[int] = None

    model_config = ConfigDict(populate_by_name=True)


class EmployeeCreate(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: str
    department: IdUrl
    employee_number: Optional[str] = Field(None, alias="employeeNumber")
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    phone_number_mobile_country: Optional[IdUrl] = Field(None, alias="phoneNumberMobileCountry")
    phone_number_mobile: Optional[str] = Field(None, alias="phoneNumberMobile")
    phone_number_home: Optional[str] = Field(None, alias="phoneNumberHome")
    phone_number_work: Optional[str] = Field(None, alias="phoneNumberWork")
    national_identity_number: Optional[str] = Field(None, alias="nationalIdentityNumber")
    dnumber: Optional[str] = None
    international_id: Optional[IdUrl] = Field(None, alias="internationalId")
    bank_account_number: Optional[str] = Field(None, alias="bankAccountNumber")
    iban: Optional[str] = None
    bic: Optional[str] = None
    creditor_bank_country_id: Optional[int] = Field(None, alias="creditorBankCountryId")
    uses_abroad_payment: Optional[bool] = Field(None, alias="usesAbroadPayment")
    user_type: Optional[IdUrl] = Field(None, alias="userType")
    allow_information_registration: Optional[bool] = Field(None, alias="allowInformationRegistration")
    is_contact: Optional[bool] = Field(None, alias="isContact")
    is_proxy: Optional[bool] = Field(None, alias="isProxy")
    comments: Optional[str] = None
    address: Optional[IdUrl] = None
    employments: Optional[List[IdUrl]] = None
    holiday_allowance_earned: Optional[IdUrl] = Field(None, alias="holidayAllowanceEarned")
    employee_category: Optional[IdUrl] = Field(None, alias="employeeCategory")
    # is_auth_project_overview_url: Optional[bool] = Field(None, alias="isAuthProjectOverviewUrl") # Removed: API rejects this field on create/update
    picture_id: Optional[int] = Field(None, alias="pictureId")

    model_config = ConfigDict(populate_by_name=True)  # Use alias for population


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    email: Optional[str] = None
    department: Optional[IdUrl] = None
    employee_number: Optional[str] = Field(None, alias="employeeNumber")
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    phone_number_mobile_country: Optional[IdUrl] = Field(None, alias="phoneNumberMobileCountry")
    phone_number_mobile: Optional[str] = Field(None, alias="phoneNumberMobile")
    phone_number_home: Optional[str] = Field(None, alias="phoneNumberHome")
    phone_number_work: Optional[str] = Field(None, alias="phoneNumberWork")
    national_identity_number: Optional[str] = Field(None, alias="nationalIdentityNumber")
    dnumber: Optional[str] = None
    international_id: Optional[IdUrl] = Field(None, alias="internationalId")
    bank_account_number: Optional[str] = Field(None, alias="bankAccountNumber")
    iban: Optional[str] = None
    bic: Optional[str] = None
    creditor_bank_country_id: Optional[int] = Field(None, alias="creditorBankCountryId")
    uses_abroad_payment: Optional[bool] = Field(None, alias="usesAbroadPayment")
    user_type: Optional[IdUrl] = Field(None, alias="userType")
    allow_information_registration: Optional[bool] = Field(None, alias="allowInformationRegistration")
    is_contact: Optional[bool] = Field(None, alias="isContact")
    is_proxy: Optional[bool] = Field(None, alias="isProxy")
    comments: Optional[str] = None
    address: Optional[IdUrl] = None
    employments: Optional[List[IdUrl]] = None
    holiday_allowance_earned: Optional[IdUrl] = Field(None, alias="holidayAllowanceEarned")
    employee_category: Optional[IdUrl] = Field(None, alias="employeeCategory")
    # is_auth_project_overview_url: Optional[bool] = Field(None, alias="isAuthProjectOverviewUrl") # Removed: API rejects this field on create/update
    picture_id: Optional[int] = Field(None, alias="pictureId")

    model_config = ConfigDict(populate_by_name=True)  # Use alias for population


class EmployeeResponse(TripletexResponse[Employee]):
    pass
