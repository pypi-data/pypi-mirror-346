import os
from typing import Type

from crudclient import API  # type: ignore[attr-defined]

from tripletex.core.client import TripletexClient
from tripletex.core.config import TripletexConfig, TripletexTestConfig
from tripletex.endpoints.activity.api import TripletexActivities
from tripletex.endpoints.country.api import TripletexCountries
from tripletex.endpoints.department.api import DepartmentApi
from tripletex.endpoints.employee.api import TripletexEmployees
from tripletex.endpoints.ledger.ledger_api import (
    TripletexAccountingPeriod,
    TripletexAnnualAccount,
    TripletexCloseGroup,
    TripletexLedger,
    TripletexPostingRules,
    TripletexVoucherType,
)
from tripletex.endpoints.project.api import TripletexProjects  # Added import
from tripletex.endpoints.supplier.api import TripletexSuppliers

class TripletexAPI(API):
    """
    Main API class for interacting with the Tripletex API.

    Provides access to various endpoints like countries, suppliers, and ledger functionalities.
    Handles client initialization and configuration.
    """

    client_class: Type[TripletexClient]
    country: TripletexCountries
    suppliers: TripletexSuppliers
    activities: TripletexActivities
    projects: TripletexProjects  # Added attribute
    department: DepartmentApi
    employee: TripletexEmployees
    ledger: TripletexLedger

    def __init__(
        self,
        client: TripletexClient | None = ...,
        client_config: TripletexConfig | TripletexTestConfig | None = ...,
        debug: bool | None = ...,
        **kwargs
    ) -> None:
        """
        Initialize the Tripletex API client.

        Args:
            client: An optional pre-configured TripletexClient instance.
            client_config: An optional configuration object (TripletexConfig or TripletexTestConfig).
                           If not provided, defaults to TripletexConfig unless debug=True.
            debug: If True, uses TripletexTestConfig by default. Defaults to False or DEBUG env var.
            **kwargs: Additional arguments passed to the base API class.
        """
        ...

    def _register_endpoints(self) -> None:
        """Registers all available API endpoints as attributes."""
        ...
