from typing import Any, Optional, Type  # Added Any, Optional

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.project.models import Project, ProjectCreate, ProjectUpdate

class TripletexProjects(TripletexCrud[Project]):
    """
    Provides CRUD operations for the Tripletex Project endpoint.

    Inherits standard GET, POST, PUT, DELETE methods from TripletexCrud.
    """

    _resource_path: str
    _datamodel: Type[Project]
    _create_model: Type[ProjectCreate]  # Renamed
    _update_model: Type[ProjectUpdate]  # Renamed

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...  # Added signature
    def _dump_data(self, data: Any, partial: bool = False) -> Any: ...  # Added signature
