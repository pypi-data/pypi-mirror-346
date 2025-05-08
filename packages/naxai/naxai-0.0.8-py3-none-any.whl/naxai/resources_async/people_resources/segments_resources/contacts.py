from typing import Optional
from pydantic import Field, validate_call


class SegmentsContactsResource:
    """contact resource for segments resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    @validate_call
    async def add(self, segment_id: str, contact_ids: list[str] = Field(min_length=1)):
        """Add contacts to a specified segment.

        This method associates one or more contacts with a segment by their IDs.

        Args:
            segment_id (str): The unique identifier of the segment to add contacts to.
            contact_ids (list[str]): A list of contact IDs to be added to the segment.

        Returns:
            The response from the API call.

        Raises:
            ValueError: If segment_id is empty or if contact_ids is empty or not a list.
            APIError: If there is an error response from the API.

        Example:
            >>> segments_contacts = SegmentsContactsResource(client, root_path)
            >>> segment_id = "seg_123abc"
            >>> contact_ids = ["cont_456def", "cont_789ghi"]
            >>> response = segments_contacts.add(segment_id, contact_ids)
        """
        return await self._client._request("POST", self.root_path + "/" + segment_id + "/addContacts", json={"ids": contact_ids}, headers=self.headers)

    @validate_call
    async def delete(self, segment_id: str, contact_ids: list[str] = Field(min_length=1)):
        """Remove contacts from a specified segment.

        This method removes one or more contacts from a segment by their IDs.

        Args:
            segment_id (str): The unique identifier of the segment to remove contacts from.
            contact_ids (list[str]): A list of contact IDs to be removed from the segment.

        Returns:
            The response from the API call.

        Raises:
            ValueError: If segment_id is empty or if contact_ids is empty or not a list.
            APIError: If there is an error response from the API.

        Example:
            >>> segments_contacts = SegmentsContactsResource(client, root_path)
            >>> segment_id = "XXXXXXXXXX"
            >>> contact_ids = ["cont_456def", "cont_789ghi"]
            >>> response = segments_contacts.delete(segment_id, contact_ids)
        """
        return await self._client._request("POST", self.root_path + "/" + segment_id + "/deleteContacts", json={"ids": contact_ids}, headers=self.headers)
    
    async def count(self, segment_id: str):
        """Count the number of contacts in a specified segment.

        This method retrieves the count of contacts associated with a segment.

        Args:
            segment_id (str): The unique identifier of the segment to count contacts for.

        Returns:
            The response from the API call containing the count of contacts.

        Raises:
            ValueError: If segment_id is empty.
            APIError: If there is an error response from the API.

        Example:
            >>> segments_contacts = SegmentsContactsResource(client, root_path)
            >>> segment_id = "XXXXXXXXXX"
            >>> response = segments_contacts.count(segment_id)
        """
        return await self._client._request("GET", self.root_path + "/" + segment_id + "/countContacts", headers=self.headers)
    
    @validate_call
    async def list(self,
                   segment_id: str,
                   page: Optional[int] = Field(default=1),
                   page_size: Optional[int] = Field(default=50),
                   sort: Optional[str] = Field(default="createdAt:desc")
                   ):
        """List contacts in a specified segment.

        This method retrieves a list of contacts associated with a segment.

        Args:
            segment_id (str): The unique identifier of the segment to list contacts for.
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of contacts to retrieve per page. Defaults to 50.
            sort (str, optional): The sorting criteria for the contacts. Defaults to "createdAt:desc".

        Returns:
            The response from the API call containing the list of contacts.

        Raises:
            ValueError: If segment_id is empty.
            APIError: If there is an error response from the API.

        Example:
            >>> segments_contacts = SegmentsContactsResource(client, root_path)
            >>> segment_id = "XXXXXXXXXX"
            >>> response = segments_contacts.list(segment_id)
        """
        params = {"page": page, "pageSize": page_size, "sort": sort}
        self._client.logger.debug("params: %s", params)
        return await self._client._request("GET", self.root_path + "/" + segment_id + "/members", headers=self.headers, params=params)