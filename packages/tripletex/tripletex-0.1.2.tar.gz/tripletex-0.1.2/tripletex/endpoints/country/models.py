from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from tripletex.core.models import Change, TripletexResponse


class Country(BaseModel):
    id: int
    version: int
    changes: Optional[List[Change]] = None
    url: str
    name: str
    display_name: Optional[str] = Field(None, alias="displayName")
    iso_alpha_2_code: Optional[str] = Field(None, alias="isoAlpha2Code")
    iso_alpha_3_code: Optional[str] = Field(None, alias="isoAlpha3Code")
    iso_numeric_code: Optional[str] = Field(None, alias="isoNumericCode")
    additional_properties: dict[str, Any] = {}

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class CountryResponse(TripletexResponse[Country]):
    pass
