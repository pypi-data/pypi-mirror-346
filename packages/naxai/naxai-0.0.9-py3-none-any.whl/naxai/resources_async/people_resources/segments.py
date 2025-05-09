import datetime
from typing import Optional
from pydantic import Field, validate_call
from naxai.models.people.create_segment import CreateSegmentRequest
from .segments_resources.contacts import SegmentsContactsResource

class SegmentsResource:
    """ segments resource for people resource """

    def __init__(self, client, root_path):
            self._client = client
            self.root_path = root_path + "/segments"
            self.headers = {"Content-Type": "application/json"}
            self.contacts = SegmentsContactsResource(client, self.root_path)

    @validate_call
    async def list(self, type_: Optional[str] = Field(default=None, alias="type"), exclude_predefined: Optional[bool] = False, attribute: Optional[str] = None ):
        """Retrieve the list of segments with optional filtering.
           Filter type can be used to retrieve manual or dynamic segments.
           exclude-predefined can be used to exclude the predefined Segments, and attribute filter is used to retrieve Segments using the given Attribute.

        Returns:
            dict: The response from the API containing the list of segments.

        Raises:
            NaxaiAPIError: If the API request fails or returns an error.
        """
        params = {"exclude-predefined": exclude_predefined}
        if type_:
            params["type"] = type_
        if attribute:
            params["attribute"] = attribute
        return await self._client._request("GET", self.root_path, headers=self.headers, params=params)
    

    async def get(self, segment_id: str):
        """Retrieves a specific segment by its ID.

        Args:
            segment_id (str): The unique identifier of the segment to retrieve.

        Returns:
            dict: The API response containing the details of the segment.

        Raises:
            NaxaiAPIError: If the API request fails or returns an error.

        Example:
            >>> segment_details = await client.people.segments.get(
            ...     segment_id="XXXXXXXXX"
            ... )
        """
        return await self._client._request("GET", self.root_path + "/" + segment_id, headers=self.headers)
            
    async def delete(self, segment_id: str):
        """Deletes a specific segment by its ID.

        Args:
            segment_id (str): The unique identifier of the segment to delete.

        Returns:
            dict: The API response confirming the deletion of the segment.

        Raises:
            NaxaiAPIError: If the API request fails or returns an error.

        Example:
            >>> deletion_result = await client.people.segments.delete(
            ...     segment_id="XXXXXXXXX"
            ... )
        """
        return await self._client._request("DELETE", self.root_path + "/" + segment_id, headers=self.headers)

    async def update(self, segment_id: str, data: CreateSegmentRequest):
        """Updates a specific segment by its ID.

        Args:
            segment_id (str): The unique identifier of the segment to update.
            data (CreateSegmentRequest): The segment update request data containing
                the necessary information to update the segment.

        Returns:
            dict: The API response containing the updated segment details.

        Raises:
            NaxaiAPIError: If the API request fails or returns an error.
        """
        return await self._client._request("PUT", self.root_path + "/" + segment_id, json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)


    async def create(self, data: CreateSegmentRequest):
        """Creates a new segment in the people resource.

        Args:
            data (CreateSegmentRequest): The segment creation request data containing
                the necessary information to create a new segment.

        Returns:
            dict: The created segment response from the API.

        Raises:
            NaxaiAPIError: If the API request fails or returns an error.
        """
        return await self._client._request("POST", self.root_path, json=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)
          
    
    async def history(self, segment_id: str,
                      start: int = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=30),
                      stop: int = datetime.datetime.now(tz=datetime.timezone.utc)):
        """Retrieve an history of contacts membership in segment by day.
           Filter with a start and stop day.

        Args:
            segment_id (str): The unique identifier of the segment to retrieve the history for.

        Returns:
            dict: The API response containing the history of the segment.

        Raises:
            NaxaiAPIError: If the API request fails or returns an error.

        Example:
            >>> segment_history = await client.people.segments.history(
            ...     segment_id="XXXXXXXXX",
                    start = 123456978,
                    stop = 123456789
            ... )
        """
        params = {"start": start, "stop": stop}
        return await self._client._request("GET", self.root_path + "/" + segment_id + "/history", headers=self.headers, params=params)
    
    async def usage(self, segment_id: str):
        """Retrieve the usage of a segment.

        Args:
            segment_id (str): The unique identifier of the segment to retrieve the usage for.

        Returns:
            dict: The API response containing the usage of the segment.

        Raises:
            NaxaiAPIError: If the API request fails or returns an error.

        Example:
            >>> segment_usage = await client.people.segments.usage(
            ...     segment_id="XXXXXXXXX"
            ... )
        """
        return await self._client._request("GET", self.root_path + "/" + segment_id + "/usage", headers=self.headers)