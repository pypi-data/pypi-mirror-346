from typing import List

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.country.models import Country, CountryResponse


class TripletexCountries(TripletexCrud[Country]):
    _resource_path = "country"
    _datamodel = Country
    _api_response_model = CountryResponse
    allowed_actions = ["list", "read"]
    _list_return_keys: List[str] = ["values"]
