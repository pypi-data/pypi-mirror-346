import logging
import os

from crudclient import API  # type: ignore[attr-defined]

from tripletex.core.client import TripletexClient
from tripletex.core.config import TripletexConfig, TripletexTestConfig
from tripletex.endpoints.activity.crud import TripletexActivities
from tripletex.endpoints.country.crud import TripletexCountries
from tripletex.endpoints.department.crud import TripletexDepartments
from tripletex.endpoints.employee.crud import TripletexEmployees
from tripletex.endpoints.ledger.crud import (
    TripletexAccount,
    TripletexAccountingPeriod,
    TripletexAnnualAccount,
    TripletexCloseGroup,
    TripletexLedger,
    TripletexPaymentTypeOut,
    TripletexPosting,
    TripletexPostingRules,
    TripletexVatType,
    TripletexVoucher,
    TripletexVoucherHistorical,
    TripletexVoucherOpeningBalance,
    TripletexVoucherType,
)
from tripletex.endpoints.project.crud import TripletexProjects
from tripletex.endpoints.supplier.crud import TripletexSuppliers

# Set up logging
logger = logging.getLogger(__name__)


class TripletexAPI(API):
    client_class = TripletexClient

    def __init__(
        self,
        client: TripletexClient | None = None,
        client_config: TripletexConfig | TripletexTestConfig | None = None,
        debug: bool | None = None,
        **kwargs
    ) -> None:

        if debug is None:
            debug = os.environ.get("DEBUG", "0") == "1"
            logger.debug("Param debug=None, setting debug=environ.DEBUG")
        if client:
            super().__init__(client=client)
            logger.debug("Initializing TripletexAPI with provided client: %r", client)
        elif client_config:
            logger.debug("Initializing TripletexAPI with provided client_config: %r", client_config)
            super().__init__(client_config=client_config)
        elif debug:
            test_config = TripletexTestConfig()
            logger.debug("Initializing TripletexAPI with debug=True, using config: %r", test_config)
            super().__init__(client_config=test_config)
        else:
            default_config = TripletexConfig()
            logger.debug("Initializing TripletexAPI with default config: %r", default_config)
            super().__init__(client_config=default_config)

    def _register_endpoints(self):
        self.activities = TripletexActivities(self.client)
        self.country = TripletexCountries(self.client)
        self.departments = TripletexDepartments(client=self.client)
        self.suppliers = TripletexSuppliers(self.client)
        self.projects = TripletexProjects(self.client)
        self.employee = TripletexEmployees(client=self.client)
        # Ledger endpoints
        self.ledger = TripletexLedger(self.client)
        self.ledger.accounting_period = TripletexAccountingPeriod(self.client, parent=self.ledger)
        self.ledger.annual_account = TripletexAnnualAccount(self.client, parent=self.ledger)
        self.ledger.close_group = TripletexCloseGroup(self.client, parent=self.ledger)
        self.ledger.voucher_type = TripletexVoucherType(self.client, parent=self.ledger)
        self.ledger.posting_rules = TripletexPostingRules(self.client, parent=self.ledger)
        self.ledger.account = TripletexAccount(self.client, parent=self.ledger)
        self.ledger.payment_type_out = TripletexPaymentTypeOut(self.client, parent=self.ledger)
        self.ledger.posting = TripletexPosting(self.client, parent=self.ledger)
        self.ledger.vat_type = TripletexVatType(self.client, parent=self.ledger)
        self.ledger.voucher = TripletexVoucher(self.client, parent=self.ledger)
        self.ledger.voucher.historical = TripletexVoucherHistorical(self.client, parent=self.ledger.voucher)
        self.ledger.voucher.opening_balance = TripletexVoucherOpeningBalance(self.client, parent=self.ledger.voucher)
