import logging
from typing import Any, Optional

from crudclient.exceptions import DataValidationError
from crudclient.response_strategies.default import DefaultResponseModelStrategy
from pydantic import ValidationError as PydanticValidationError

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.activity.models import (
    Activity,
    ActivityCreate,
    ActivityResponse,
)

logger = logging.getLogger(__name__)


class TripletexActivities(TripletexCrud[Activity]):
    _resource_path = "activity"
    _datamodel = Activity
    _create_model = ActivityCreate
    allowed_actions = ["list", "read", "create"]
    _list_key = "values"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # Explicitly configure the response strategy to handle the 'values' key for lists
        self._response_strategy = DefaultResponseModelStrategy(
            datamodel=self._datamodel, api_response_model=ActivityResponse, list_return_keys=[self._list_key]
        )

    def _dump_data(self, data: Any, partial: bool = False) -> Any:
        # Docstring moved to .pyi file
        model_to_use: Optional[type] = None  # Explicit type hint
        if not partial and hasattr(self, "_create_model") and self._create_model:
            model_to_use = self._create_model
        elif partial and hasattr(self, "_update_model") and self._update_model:
            # Note: Activity endpoint doesn't have _update_model, but keep this logic for consistency/future use.
            model_to_use = self._update_model

        if model_to_use:
            logger.debug(f"Attempting validation and dumping with {model_to_use.__name__} (partial={partial})")
            try:
                # Validate data against the chosen model
                instance = model_to_use.model_validate(data)
                # Dump the validated instance to a dict suitable for JSON serialization
                # Pydantic v2 uses model_dump
                dumped_data = instance.model_dump(mode="json", exclude_unset=partial)
                logger.debug(f"Data validated and dumped successfully using {model_to_use.__name__}")
                return dumped_data
            except PydanticValidationError as e:
                # Simplified error logging due to removed redaction
                error_message = f"Data validation failed using {model_to_use.__name__}. Errors: {e}"
                logger.error(error_message)
                # Raise a more generic DataValidationError for the client layer
                raise DataValidationError(error_message) from e
        else:
            # Fallback to default behavior if no specific model is found or applicable
            logger.debug("No specific create/update model found/applicable, falling back to super()._dump_data")
            return super()._dump_data(data, partial=partial)
