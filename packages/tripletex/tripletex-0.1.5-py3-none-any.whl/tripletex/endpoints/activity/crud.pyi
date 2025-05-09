from typing import Any, ClassVar, List, Type

from crudclient.response_strategies.default import DefaultResponseModelStrategy

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.activity.models import Activity, ActivityCreate

class TripletexActivities(TripletexCrud[Activity]):
    """Provides API methods for interacting with activities."""

    _resource_path: ClassVar[str]
    _datamodel: ClassVar[Type[Activity]]
    _create_model: ClassVar[Type[ActivityCreate]]
    allowed_actions: ClassVar[List[str]]
    _list_key: ClassVar[str]
    _response_strategy: DefaultResponseModelStrategy  # Instance variable, but annotated here for mypy

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def _dump_data(self, data: Any, partial: bool = False) -> Any:
        """Validates and prepares data for JSON serialization using Pydantic models."""
        ...
