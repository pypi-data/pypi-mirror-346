from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from tripletex.core.models import IdRef, IdUrl
from tripletex.endpoints.employee.models import Employee


# Base model with common fields used in Create, Update, and Response
class ProjectBase(BaseModel):
    name: str
    number: Optional[str] = None
    start_date: Optional[date] = Field(None, alias="startDate")
    end_date: Optional[date] = Field(None, alias="endDate")
    is_closed: Optional[bool] = Field(None, alias="isClosed")
    is_offer: Optional[bool] = Field(None, alias="isOffer")
    is_fixed_price: Optional[bool] = Field(None, alias="isFixedPrice")
    # Note: Add other common fields if identified


# Model for creating a project (Payload for POST)
# Does NOT inherit from ProjectBase as API rejects fields like customerId, projectManagerId etc. on create
class ProjectCreate(BaseModel):
    name: str
    number: Optional[str] = None
    project_manager: IdRef = Field(..., alias="projectManager")
    # Only include fields explicitly allowed/required by POST /v2/project


# Model for updating a project (Payload for PUT)
# Assuming PUT requires all fields similar to Create
class ProjectUpdate(ProjectCreate):
    pass


# Model representing a project as returned by the API (Response for GET, POST, PUT)
class Project(ProjectBase):
    id: int
    version: int
    # Optional related objects often returned by GET requests
    # Use IdUrl or specific models depending on API response structure
    customer: Optional[IdUrl] = None  # Customer might be IdUrl or full Customer object
    project_manager: Optional[Employee] = Field(None, alias="projectManager")
    department: Optional[IdUrl] = None  # Department might be IdUrl or full Department object
    # Note: Add other fields returned by GET /project/{id} if known
