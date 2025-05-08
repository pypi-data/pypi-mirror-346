# -*- coding: utf-8 -*-
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
    _resource_path = "company"
    _datamodel = Company
    # No create model specified in the task context
    _update_model = CompanyUpdate
    _api_response_model = TripletexCompanyResponse
    # Based on GET /company/{id} (read) and PUT /company (update)
    allowed_actions = ["read", "update"]

    def get_divisions(
        self,
        **kwargs: Any,
    ) -> TripletexCompanyDivisionListResponse:
        # Use custom_action for non-standard GET requests
        response_data = self.custom_action(
            action="divisions",  # Path segment after resource_path
            method="GET",
            params=kwargs,
        )
        # Manually validate the response against the specific list model
        return TripletexCompanyDivisionListResponse.model_validate(response_data)

    def get_with_login_access(
        self,
        **kwargs: Any,
    ) -> TripletexCompanyWithLoginAccessListResponse:
        # Use custom_action for non-standard GET requests
        # Note: The '>' character is part of the action path segment
        response_data = self.custom_action(
            action=">withLoginAccess",
            method="GET",
            params=kwargs,
        )
        # Manually validate the response against the specific list model
        return TripletexCompanyWithLoginAccessListResponse.model_validate(response_data)

    # Standard get(id) and update(body) are handled by TripletexCrud
    # based on allowed_actions = ["read", "update"]
