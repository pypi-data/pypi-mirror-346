from typing import Optional
from pydantic import Field, validate_call

class BouncesResource:
    """ bounces resource for email.suppression_lists resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/bounces"
        self.headers = {"Content-Type": "application/json"}
    
    #TODO: email validation
    @validate_call
    async def list(self,
                   page: Optional[int] = 1,
                   page_size: Optional[int] = Field(default=50, ge=1, le=100),
                   email: Optional[str] = None
                   ):
        """
        Retrieves a list of bounces for a given time period and filters.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 100.
            email (str, optional): The email address to filter on.

        Returns:
            dict: The API response containing the list of bounces.

        Example:
            >>> response = await client.email.suppression_lists.bounces.list(start=1625097600, stop=1627689600)
        """
        params = {
            "page": page,
            "pagesize": page_size
        }

        if email:
             params["email"] = email

        return await self._client._request("GET", self.root_path, params=params, headers=self.headers)