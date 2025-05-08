# -*- coding: utf-8 -*-
"""Company endpoint models."""
from typing import List, TypeAlias

from pydantic import BaseModel

from tripletex.core.models import TripletexResponse

# Placeholder models due to missing Swagger schemas
class Company(BaseModel):
    """Placeholder model for a Company."""

    ...  # Add fields later if discovered

class CompanyDivision(BaseModel):
    """Placeholder model for a Company Division."""

    ...  # Add fields later if discovered

class CompanyWithLoginAccess(BaseModel):
    """Placeholder model for Company With Login Access."""

    ...  # Add fields later if discovered

class CompanyUpdate(BaseModel):
    """Placeholder model for updating a Company (request body)."""

    ...  # Add fields later if discovered

# Response Wrappers
TripletexCompanyResponse: TypeAlias = TripletexResponse[Company]
TripletexCompanyDivisionListResponse: TypeAlias = TripletexResponse[List[CompanyDivision]]
TripletexCompanyWithLoginAccessListResponse: TypeAlias = TripletexResponse[List[CompanyWithLoginAccess]]
# Note: PUT /company likely returns the updated company,
# so its response would use TripletexCompanyResponse.
# Note: PUT /company request body would use CompanyUpdate.
