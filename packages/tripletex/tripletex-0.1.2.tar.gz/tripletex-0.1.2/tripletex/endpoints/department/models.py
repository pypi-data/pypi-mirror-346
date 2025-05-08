from typing import Optional

from pydantic import BaseModel, ConfigDict

from tripletex.core.models import TripletexResponse


class Department(BaseModel):
    id: int
    version: int
    url: str
    name: str
    model_config = ConfigDict(populate_by_name=True)


class DepartmentCreate(BaseModel):
    name: str


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None


class DepartmentResponse(TripletexResponse[Department]):
    pass
