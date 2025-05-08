from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class TripletexResponse(BaseModel, Generic[T]):
    full_result_size: Optional[int] = Field(None, alias="fullResultSize")
    from_index: Optional[int] = Field(None, alias="from")
    count: int
    version_digest: Optional[str] = Field(None, alias="versionDigest")
    values: List[T]

    model_config = ConfigDict(populate_by_name=True)


class IdRef(BaseModel):
    """
    Model for referencing an object in a different object.
    Analogous to a foreign key in a database.
    This model is used to represent a reference to an object by its ID.
    For example, in a JSON response, it might look like:
    {
        "id": 123
    }
    This is a simplified model that only contains the ID of the referenced object.
    It is typically used in APIs to represent relationships between objects.

    Attributes:
        id: Unique identifier of the account.
    """

    id: int

    model_config = ConfigDict(populate_by_name=True)


class IdUrl(BaseModel):
    id: int
    url: str


class Change(BaseModel):
    employee_id: Optional[int] = Field(None, alias="employeeId")
    timestamp: Optional[str] = None
    change_type: Optional[str] = Field(None, alias="changeType")
