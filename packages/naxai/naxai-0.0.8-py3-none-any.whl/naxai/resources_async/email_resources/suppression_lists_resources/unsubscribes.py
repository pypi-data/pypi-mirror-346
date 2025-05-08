from typing import Optional
from pydantic import Field, validate_call
from naxai.models.email.create_email_supression_lists_unsubscribe import CreateEmailSuppressionListsUnsubscribe

class UnsubscribesResource:
    """ unsubscribes resource for email.suppression_lists resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/unsubscribes"
        self.headers = {"Content-Type": "application/json"}
            
    async def delete(self, data: list[CreateEmailSuppressionListsUnsubscribe]):
        """
        Deletes unsubscribes for a given list of email addresses.

        Args:
            data (list[CreateEmailSuppressionListsUnsubscribe]): A list of email addresses to delete.

        Returns:
            dict: The API response indicating the success of the deletion.

        Example:
            >>> response = await client.email.suppression_lists.unsubscribes.delete(data)
        """
        return await self._client._request("POST", self.root_path + "/remove", json={"recipients": data}, headers=self.headers)
        
        
    async def create(self, data: CreateEmailSuppressionListsUnsubscribe):
        """
        Creates a new unsubscribe for a given email address.

        Args:
            data (CreateEmailSuppressionListsUnsubscribe): The data for the new unsubscribe.

        Returns:
            dict: The API response indicating the success of the creation.

        Example:
            >>> response = await client.email.suppression_lists.unsubscribes.create(data)
        """
        return await self._client._request("POST", self.root_path + "/add", json=data.model_dump(exclude_none=True, by_alias=True), headers=self.headers)
    
    @validate_call
    async def list(self,
                   page: Optional[int] = 1,
                   page_size: Optional[int] = Field(default=50, ge=1, le=100),
                   email: Optional[str] = None):
        """
        Retrieves a list of unsubscribes for a given time period and filters.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 50.
            email: (str, optional): The email address to filter on.

        Returns:
            dict: The API response containing the list of unsubscribes.

        Example:
            >>> response = await client.email.suppression_lists.unsubscribes.list(start=1625097600, stop=1627689600)
        """
        params = {
            "page": page,
            "pagesize": page_size
        }

        if email:
             params["email"] = email

        return await self._client._request("GET", self.root_path, params=params, headers=self.headers)