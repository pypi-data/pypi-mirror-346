from typing import TypeVar

from crudclient import Crud, JSONDict, RawResponse  # type: ignore[attr-defined]

T = TypeVar("T")

class TripletexCrud(Crud[T]):
    """
    Tripletex-specific CRUD operations base class.
    Overrides response conversion to handle the 'value' wrapper in Tripletex responses.
    """

    def _convert_to_model(self, data: RawResponse) -> T | JSONDict:
        """
        TripleTex-specific method to convert API response to data model.

        Extracts the actual data from the 'value' field if present,
        then converts it to the specified datamodel or returns the raw dictionary.

        Args:
            data: The raw response data from the API.

        Returns:
            An instance of the datamodel T or the raw JSON dictionary.

        Raises:
            ValueError: If the validated response data is not a dictionary.
        """
        ...
