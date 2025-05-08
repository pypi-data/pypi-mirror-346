from typing import List

from tripletex.core.crud import TripletexCrud
from tripletex.endpoints.country.models import Country

class TripletexCountries(TripletexCrud[Country]):
    _list_return_keys: List[str]
