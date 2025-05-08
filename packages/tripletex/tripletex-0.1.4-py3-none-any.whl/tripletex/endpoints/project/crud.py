import logging
from typing import Any, ClassVar, Optional, Type  # Added ClassVar, List, Type

from crudclient.exceptions import DataValidationError
from crudclient.response_strategies.default import DefaultResponseModelStrategy

# Imports needed for exception handling and base classes
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.project.models import Project, ProjectCreate, ProjectUpdate

# Imports needed for exception handling and base classes


logger = logging.getLogger(__name__)


class TripletexProjects(TripletexCrud[Project]):
    """
    Provides CRUD operations for the Tripletex Project endpoint.

    Inherits standard GET, POST, PUT, DELETE methods from TripletexCrud.
    """

    _resource_path: ClassVar[str] = "/project"
    _datamodel: ClassVar[Type[Project]] = Project
    _create_model: ClassVar[Type[ProjectCreate]] = ProjectCreate
    _update_model: ClassVar[Type[ProjectUpdate]] = ProjectUpdate
    # _list_response_key = "values" # Setting via response_strategy instead

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the TripletexProjects endpoint, configuring the response strategy.
        """
        super().__init__(*args, **kwargs)
        # Explicitly configure the response strategy to handle the 'values' key for lists
        # Assuming no specific ProjectResponse model for now
        self._response_strategy = DefaultResponseModelStrategy(datamodel=self._datamodel, list_return_keys=["values"])

    def _dump_data(self, data: Any, partial: bool = False) -> Any:
        """
        Validate and dump data using create/update models if available.

        Overrides the default behavior to use `_create_model` for full updates
        and `_update_model` for partial updates, falling back to the superclass
        method if the specific models are not defined or applicable.

        Args:
            data: The data to validate and dump.
            partial: If True, use the update model and exclude unset fields.
                     If False, use the create model.

        Returns:
            The validated and dumped data suitable for JSON serialization.

        Raises:
            DataValidationError: If validation fails against the chosen model.
        """
        # Standard logic: Determine model, validate, then dump
        model_to_use: Optional[type[BaseModel]] = None
        if not partial and hasattr(self, "_create_model") and self._create_model:
            model_to_use = self._create_model
        elif partial and hasattr(self, "_update_model") and self._update_model:
            model_to_use = self._update_model

        if model_to_use:
            logger.debug(f"Attempting validation and dumping with {model_to_use.__name__} (partial={partial})")
            try:
                instance = model_to_use.model_validate(data)  # Validate input (dict or model)

                # Determine exclude_unset based on operation type
                # Create should include all fields (exclude_unset=False)
                # Update should only include explicitly set fields (exclude_unset=True)
                exclude_unset_flag = model_to_use == self._update_model

                dumped_data = instance.model_dump(mode="json", exclude_unset=exclude_unset_flag, by_alias=True)
                logger.debug(f"Data validated and dumped successfully using {model_to_use.__name__}: {dumped_data}")
                return dumped_data
            except PydanticValidationError as e:
                error_message = f"Data validation failed using {model_to_use.__name__}. Errors: {e}"
                logger.error(error_message)
                raise DataValidationError(error_message, data=data) from e
        else:
            logger.debug("No specific create/update model found/applicable, falling back to super()._dump_data")
            return super()._dump_data(data, partial=partial)
