"""Core data models used across various Tripletex endpoints."""

from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")

class TripletexResponse(BaseModel, Generic[T]):
    """
    Represents a standard paginated response structure from the Tripletex API.

    Attributes:
        full_result_size: The total number of items available across all pages.
        from_index: The starting index of the items included in this response page.
        count: The number of items included in this response page.
        version_digest: A digest representing the version of the data.
        values: A list containing the actual data objects for this page.
    """

    full_result_size: Optional[int] = Field(None, alias="fullResultSize")
    from_index: Optional[int] = Field(None, alias="from")
    count: int
    version_digest: Optional[str] = Field(None, alias="versionDigest")
    values: List[T]

    model_config = ConfigDict(populate_by_name=True)

class IdUrl(BaseModel):
    """
    A simple model representing an object with an ID and a URL.

    Attributes:
        id: The unique identifier of the object.
        url: The URL pointing to the object resource.
    """

    id: int
    url: str

class Change(BaseModel):
    """
    Represents a change record, often associated with creation or modification history.

    Attributes:
        employee_id: The ID of the employee who made the change.
        timestamp: The timestamp when the change occurred.
        change_type: The type of change made (e.g., 'CREATED', 'UPDATED').
    """

    employee_id: Optional[int] = Field(None, alias="employeeId")
    timestamp: Optional[str] = None
    change_type: Optional[str] = Field(None, alias="changeType")

# Simple model for referencing an object by ID, e.g., {"id": 1}
class IdRef(BaseModel):
    """
    A simple model representing a reference to another object by its ID.

    Attributes:
        id: The unique identifier of the referenced object.
    """

    id: int
