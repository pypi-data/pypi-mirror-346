from typing import Optional, Literal
from pydantic import Field, validate_call
from naxai.models.people.search_condition import SearchCondition

class ExportsResource:
    """ exports resource for people resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/exports"
        self.headers = {"Content-Type": "application/json"}

    async def list(self):
        """
        List all exports for people resource.

        Returns:
            dict: The API response containing the list of exports

        Example:
            >>> response = await client.people.exports.list()
        """
        return await self._client._request("GET", self.root_path, headers=self.headers)
    
    async def create(self, condition: SearchCondition):
        """
        Create a new export for people resource.

        Args:
            condition (SearchCondition): The search condition for the export

        Returns:
            dict: The API response containing the created export details

        Example:
            >>> response = await client.people.exports.create(condition=SearchCondition())
        """
        return await self._client._request("POST", self.root_path, json=condition.model_dump(by_alias=True, exclude_none=True), headers=self.headers)
    
    async def get(self, export_id: str):
        """
        Get details of a specific export for people resource.

        Args:
            export_id (str): The ID of the export to retrieve

        Returns:
            dict: The API response containing the export details

        Example:
            >>> response = await client.people.exports.get(export_id="XXXX")
        """
        return await self._client._request("GET", self.root_path + "/" + export_id, headers=self.headers)
    

    async def get_download_url(self, export_id: str):
        """
        Get the download URL for a specific export of people resource.

        Args:
            export_id (str): The ID of the export to retrieve the download URL for

        Returns:
            dict: The API response containing the download URL

        Example:
            >>> response = await client.people.exports.get_download_url(export_id="XXXX")
        """
        return await self._client._request("GET", self.root_path + "/" + export_id + "/download", headers=self.headers)