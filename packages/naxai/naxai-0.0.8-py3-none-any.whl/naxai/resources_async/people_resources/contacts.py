from typing import Optional, Union
from pydantic import Field, validate_call
from naxai.models.people.search_condition import SearchCondition
from .contacts_resources.events import EventsResource
from .contacts_resources.identifier import IdentifierResource
from .contacts_resources.segments import SegmentsResource

class ContactsResource:
    """ contacts resource for people resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/contacts"
        self.headers = {"Content-Type": "application/json"}
        self.events: EventsResource = EventsResource(client, self.root_path)
        self.identifier: IdentifierResource = IdentifierResource(client, self.root_path)
        self.segments: SegmentsResource = SegmentsResource(client, self.root_path)

    @validate_call
    async def search(self,
                     page: Optional[int] = Field(default=1, gt=1),
                     page_size: Optional[int] = Field(default=50, gt=1),
                     sort: Optional[str] = Field(default="createdAt:desc"),
                     condition: Optional[Union[dict, SearchCondition]] = Field(default=None)):
        """
        Search for contacts based on specified conditions.

        Args:
            page (int, optional): The page number for pagination. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 50.
            sort (str, optional): The sorting criteria. Defaults to "createdAt:desc".
            condition (Union[dict, SearchCondition], optional): The search condition. Defaults to None.

        Returns:
            dict: The API response containing the search results.

        Raises:
            ValueError: If the condition is not a dictionary or SearchCondition object.
            APIError: If there is an error response from the API.

        Example:
            >>> search_result = client.people.contacts.search(
            ...     page=1,
            ...     page_size=50,
            ...     sort="createdAt:desc",
            ...     condition={"name": "John Doe"}
            ... )
        """
        params = {"page": page, "pageSize": page_size, "sort": sort}

        body_params = condition.model_dump(by_alias=True, exclude_none=True) if isinstance(condition, SearchCondition) else condition
        if body_params:
            json_body = {"condition": condition}
            return await self._client._request("POST", self.root_path, params=params, json=json_body, headers=self.headers)
        else:
             return await self._client._request("POST", self.root_path, params=params, headers=self.headers)
        

    async def count(self):
        """
        Get the total count of contacts.

        Returns:
            dict: The API response containing the total count of contacts.

        Example:
            >>> count = client.people.contacts.count()
        """
        return await self._client._request("GET", self.root_path + "/count", headers=self.headers)
    
    #TODO: email validation, phone validation
    @validate_call
    async def create_or_update(self,
                               identifier: str,
                               email: Optional[str] = None,
                               external_id: Optional[str] = None,
                               unsubscribe: Optional[bool] = None,
                               language: Optional[str] = None,
                               created_at: Optional[int] = Field(ge=2208988800, le=4102444800, default=None),
                               **kwargs):
        """
        Create or update a contact.

        Args:
            identifier (str): The unique identifier for the contact.
            email (str, optional): The email address of the contact.
            external_id (str, optional): The external ID of the contact.
            unsubscribe (bool, optional): Whether the contact is unsubscribed.
            language (str, optional): The language of the contact.
            created_at (int, optional): The creation timestamp of the contact. Defaults to 2208988800.
            **kwargs: Additional keyword arguments for other contact details.

        Returns:
            dict: The API response containing the created or updated contact details.

        Raises:
            ValueError: If the identifier is empty.
            APIError: If there is an error response from the API.

        Example:
            >>> response = client.people.contacts.create_or_update(
            ...     identifier="XXXX",
            ...     email="XXXX",
            ...     external_id="XXXX",
            ...     unsubscribe=True,
            ...     language="XXXX",
            ...     created_at=XXXX,
            ...     **kwargs
            ... )
        """
        data = {
            "email": email,
            "externalId": external_id,
            "unsubscribe": unsubscribe,
            "language": language,
            "createdAt": created_at,
            **kwargs
        }
        return await self._client._request("PUT", self.root_path + "/" + identifier, json=data, headers=self.headers)
    
    async def get(self, identifier: str):
            """
            Get a contact by identifier.

            Args:
                identifier (str): The unique identifier of the contact.

            Returns:
                dict: The API response containing the contact details.

            Raises:
                ValueError: If the identifier is empty.
                APIError: If there is an error response from the API.

            Example:
                >>> contact = client.people.contacts.get(identifier="XXXX")
            """
            return await self._client._request("GET", self.root_path + "/" + identifier, headers=self.headers)
    
    async def delete(self, identifier: str):
        """
        Delete a contact by identifier.

        Args:
            identifier (str): The unique identifier of the contact.

        Returns:
            dict: The API response indicating the deletion status.

        Raises:
            ValueError: If the identifier is empty.
            APIError: If there is an error response from the API.

        Example:
            >>> response = client.people.contacts.delete(identifier="XXXX")
        """
        return await self._client._request("DELETE", self.root_path + "/" + identifier, headers=self.headers)
    

        
