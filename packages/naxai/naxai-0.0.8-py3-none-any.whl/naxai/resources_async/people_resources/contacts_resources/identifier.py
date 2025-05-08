class IdentifierResource:
    """identifier resource for people.contacts resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/keyIdentifier"
        self.headers = {"Content-Type": "application/json"}

    #TODO: check this method ... and get information
    async def get(self):
        """Retrieve key identifier information.

        This asynchronous method fetches the key identifier data from the API endpoint.

        Returns:
            

        Raises:
            APIError: If there is an error response from the API.

        Example:
            >>> identifier_data = await client.people.contacts.identifier.get()

        Note:
            This method is a coroutine and must be called using await.
        """

        return await self._client._request("GET", self.root_path, headers=self.headers)
    
    #TODO: check this method ... and get information
    async def update(self):
        """Update key identifier information.

        This asynchronous method sends a PUT request to the API endpoint to update the key identifier data.

        Returns:
            dict: The response containing the updated key identifier information.
                The specific structure of the response will depend on the API implementation.

        Raises:
            APIError: If there is an error response from the API.
            ConnectionError: If there are network connectivity issues.

        Example:
            >>> updated_identifier_data = await client.people.contacts.identifier.update()

        Note:
            This method is a coroutine and must be called using await.
        """

        return await self._client._request("PUT", self.root_path, headers=self.headers)
    