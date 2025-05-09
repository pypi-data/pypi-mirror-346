from typing import Optional, Literal
from pydantic import Field, validate_call

class AttributesResource:
    """ attributes resource for people resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/attributes"
        self.headers = {"Content-Type": "application/json"}
        
    async def delete(self, name: str):
        """
        Delete an attribute for people resource.

        Args:
            name (str): The name of the attribute to delete

        Returns:
            dict: The API response containing the deleted attribute details

        Example:
            >>> response = await client.people.attributes.delete(name="favorite_color")
        """
        return await self._client._request("DELETE", self.root_path + "/" + name, headers=self.headers)
    
    async def get(self, name: str):
        """
        Get a specific attribute for people resource.

        Args:
            name (str): The name of the attribute to retrieve

        Returns:
            dict: The API response containing the attribute details

        Example:
            >>> response = await client.people.attributes.get(name="favorite_color")
        """
        return await self._client._request("GET", self.root_path + "/" + name, headers=self.headers)
        
    async def list(self):
        """
        List all attributes for people resource.

        Returns:
            dict: The API response containing the list of attributes

        Example:
            >>> response = await client.people.attributes.list()
        """
        return await self._client._request("GET", self.root_path, headers=self.headers)
        
    async def create(self, name: str):
        """
        Create a new attribute for people resource.

        Args:
            name (str): The name of the attribute to create

        Returns:
            dict: The API response containing the created attribute details

        Example:
            >>> response = await client.people.attributes.create(name="favorite_color")
        """
        return await self._client._request("POST", self.root_path, json={"name": name}, headers=self.headers)