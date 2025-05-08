# -*- coding: utf-8 -*-
"""API Logic for /company endpoint."""
from typing import Any

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.company.models import (
    Company,
    CompanyUpdate,
    TripletexCompanyDivisionListResponse,
    TripletexCompanyResponse,
    TripletexCompanyWithLoginAccessListResponse,
)

class CompanyApi(TripletexCrud[Company]):
    """API Logic for /company endpoint."""

    _resource_path: str
    _datamodel: type[Company]
    _update_model: type[CompanyUpdate]
    _api_response_model: type[TripletexCompanyResponse]
    allowed_actions: list[str]

    def get_divisions(
        self,
        **kwargs: Any,
    ) -> TripletexCompanyDivisionListResponse:
        """Fetch divisions for the company.

        Args:
            **kwargs: Additional query parameters.

        Returns:
            TripletexCompanyDivisionListResponse: Response containing a list of divisions.
        """
        ...

    def get_with_login_access(
        self,
        **kwargs: Any,
    ) -> TripletexCompanyWithLoginAccessListResponse:
        """Fetch companies the user has login access to.

        Args:
            **kwargs: Additional query parameters.

        Returns:
            TripletexCompanyWithLoginAccessListResponse: Response containing a list of companies.
        """
        ...
    # Standard get(id) and update(body) are handled by TripletexCrud
    # based on allowed_actions = ["read", "update"]
