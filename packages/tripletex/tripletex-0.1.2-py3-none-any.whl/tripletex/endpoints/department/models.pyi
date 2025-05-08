"""Pydantic models for the Tripletex Department endpoint."""

from typing import ClassVar, Optional

from pydantic import BaseModel, ConfigDict

from tripletex.core.models import TripletexResponse

class Department(BaseModel):
    """Represents a department resource in Tripletex."""

    id: int
    version: int
    url: str
    name: str
    model_config: ClassVar[ConfigDict]

class DepartmentCreate(BaseModel):
    """Data required to create a new department."""

    name: str

class DepartmentUpdate(BaseModel):
    """Data allowed when updating an existing department."""

    name: Optional[str]

class DepartmentResponse(TripletexResponse[Department]):
    """Response wrapper for single department results."""

    pass
