# -*- coding: utf-8 -*-
from typing import Any, ClassVar

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.company.models import (
    Company,
    CompanyListResponse,
    CompanyResponse,
    CompanyUpdate,
)


class CompanyApi(TripletexCrud[Company]):
    """API Logic for /company endpoint."""

    _resource_path: str = "company"
    _datamodel: ClassVar[type[Company]] = Company
    # No create model specified in the task context
    _update_model: ClassVar[type[CompanyUpdate]] = CompanyUpdate
    _api_response_model: ClassVar[type[CompanyResponse]] = CompanyResponse
    # Based on GET /company/{id} (read) and PUT /company (update)
    allowed_actions: list[str] = ["read", "update"]

    def get_divisions(
        self,
        **kwargs: Any,
    ) -> CompanyListResponse:
        """Fetch divisions for the company.

        Args:
            **kwargs: Additional query parameters.

        Returns:
            CompanyListResponse: Response containing a list of divisions.
        """
        # Use custom_action for non-standard GET requests
        response_data = self.custom_action(
            action="divisions",  # Path segment after resource_path
            method="GET",
            params=kwargs,
        )
        # Manually validate the response against the specific list model
        return CompanyListResponse.model_validate(response_data)

    def get_with_login_access(
        self,
        **kwargs: Any,
    ) -> CompanyListResponse:
        """Fetch companies the user has login access to.

        Args:
            **kwargs: Additional query parameters.

        Returns:
            TripletexCompanyWithLoginAccessListResponse: Response containing a list of companies.
        """
        # Use custom_action for non-standard GET requests
        # Note: The '>' character is part of the action path segment
        response_data = self.custom_action(
            action=">withLoginAccess",
            method="GET",
            params=kwargs,
        )
        # Manually validate the response against the specific list model
        return CompanyListResponse.model_validate(response_data)

    # Standard get(id) and update(body) are handled by TripletexCrud
    # based on allowed_actions = ["read", "update"]
