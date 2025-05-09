from typing import Optional, Literal
from pydantic import Field, validate_call

class ImportsResource:
    """ imports resource for people resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/imports"
        self.headers = {"Content-Type": "application/json"}

    async def list(self):
        """
        List all imports for people resource.

        Returns:
            dict: The API response containing the list of imports

        Example:
            >>> response = await client.people.imports.list()
        """
        return await self._client._request("GET", self.root_path, headers=self.headers)

    async def get(self, import_id: str):
        """
        Get a specific import for people resource.

        Args:
            import_id (str): The ID of the import to retrieve

        Returns:
            dict: The API response containing the import details

        Example:
            >>> response = await client.people.imports.get(import_id="XXXX")
        """
        return await self._client._request("GET", self.root_path + "/" + import_id, headers=self.headers)