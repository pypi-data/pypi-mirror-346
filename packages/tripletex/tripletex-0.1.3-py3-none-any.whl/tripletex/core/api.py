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
    """
    Main API class for interacting with the Tripletex API.

    Provides access to various endpoints like countries, suppliers, and ledger functionalities.
    Handles client initialization and configuration.
    """

    client_class = TripletexClient

    def __init__(
        self,
        client: TripletexClient | None = None,
        client_config: TripletexConfig | TripletexTestConfig | None = None,
        debug: bool | None = None,
        rate_limiter=None,  # FileBasedRateLimiter or compatible object
        mp_lock=None,
        mp_remaining=None,
        mp_reset_timestamp=None,
        num_workers: int = 1,
        buffer_size: int = 10,
        **kwargs,
    ) -> None:
        """
        Initialize the Tripletex API client.

        Args:
            client: An optional pre-configured TripletexClient instance.
            client_config: An optional configuration object (TripletexConfig or TripletexTestConfig).
                           If not provided, defaults to TripletexConfig unless debug=True.
            debug: If True, uses TripletexTestConfig by default. Defaults to False or DEBUG env var.
            rate_limiter: A rate limiter object for API rate limiting.
            mp_lock: A multiprocessing lock for rate limiting coordination.
            mp_remaining: A multiprocessing Value for tracking API rate limit remaining calls.
            mp_reset_timestamp: A multiprocessing Value for tracking API rate limit reset timestamp.
            num_workers: Number of worker processes for dynamic threshold calculation.
            buffer_size: Buffer size for rate limit threshold.
            **kwargs: Additional arguments passed to the base API class.
        """

        if debug is None:
            debug = os.environ.get("DEBUG", "0") == "1"
            logger.debug("Param debug=None, setting debug=environ.DEBUG")
        if client:
            super().__init__(client=client)
            logger.debug("Initializing TripletexAPI with provided client: %r", client)

            # Store rate limiting parameters for potential use in API subclass
            self.rate_limiter = rate_limiter
            self.mp_lock = mp_lock
            self.mp_remaining = mp_remaining
            self.mp_reset_timestamp = mp_reset_timestamp
            self.num_workers = num_workers
            self.buffer_size = buffer_size
        elif client_config:
            logger.debug("Initializing TripletexAPI with provided client_config: %r", client_config)
            super().__init__(
                client_config=client_config,
                rate_limiter=rate_limiter,
                mp_lock=mp_lock,
                mp_remaining=mp_remaining,
                mp_reset_timestamp=mp_reset_timestamp,
                num_workers=num_workers,
                buffer_size=buffer_size,
                **kwargs,
            )
        elif debug:
            test_config = TripletexTestConfig()
            logger.debug("Initializing TripletexAPI with debug=True, using config: %r", test_config)
            super().__init__(
                client_config=test_config,
                rate_limiter=rate_limiter,
                mp_lock=mp_lock,
                mp_remaining=mp_remaining,
                mp_reset_timestamp=mp_reset_timestamp,
                num_workers=num_workers,
                buffer_size=buffer_size,
                **kwargs,
            )
        else:
            default_config = TripletexConfig()
            logger.debug("Initializing TripletexAPI with default config: %r", default_config)
            super().__init__(
                client_config=default_config,
                rate_limiter=rate_limiter,
                mp_lock=mp_lock,
                mp_remaining=mp_remaining,
                mp_reset_timestamp=mp_reset_timestamp,
                num_workers=num_workers,
                buffer_size=buffer_size,
                **kwargs,
            )

    def _initialize_client(self) -> None:
        """Override the parent _initialize_client method to pass rate limiting parameters."""
        logger.debug("Initializing client with rate limiting parameters")

        # Check if client_class is defined (parent class check)
        if not hasattr(self, "client_class") or self.client_class is None:
            logger.error("client_class is not defined. Cannot initialize the client.")
            raise Exception("Cannot initialize client because client_class is not set.")

        # Check if client_config is defined (parent class check)
        if not self.client_config:
            logger.error("client_config is not defined. Cannot initialize the client.")
            raise Exception("Cannot initialize client because client_config is not set.")

        logger.debug(f"Initializing API class with client class {self.client_class.__name__}, using client_config: {self.client_config}")

        try:
            # Initialize client with rate limiting parameters
            rate_limiter = getattr(self, "rate_limiter", None)
            if rate_limiter is not None:
                logger.info("Using rate limiter for client initialization")
                self.client = self.client_class(
                    config=self.client_config,
                    rate_limiter=rate_limiter,
                    num_workers=getattr(self, "num_workers", 1),
                    buffer_size=getattr(self, "buffer_size", 10),
                )
            else:
                # Initialize without rate limiting
                logger.warning("Initializing client WITHOUT rate limiting - API rate limits may be exceeded")
                self.client = self.client_class(
                    config=self.client_config,
                    num_workers=getattr(self, "num_workers", 1),
                    buffer_size=getattr(self, "buffer_size", 10),
                )
        except Exception as e:
            logger.exception("Failed to initialize the client.")
            raise Exception("Failed to initialize the client.") from e

        logger.info("Client initialized successfully with rate limiting parameters.")

    def _register_endpoints(self) -> None:
        """Registers all available API endpoints as attributes."""
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
