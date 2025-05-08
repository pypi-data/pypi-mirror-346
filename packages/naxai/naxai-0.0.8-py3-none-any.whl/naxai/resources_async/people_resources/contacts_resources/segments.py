class SegmentsResource:
    """ segments resource for people.contacts resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    async def list(self, identifier: str):
        """Retrieve the list of segments associated to a contact.


        Args:
            identifier (str): The unique identifier of contact.

        Returns:


        Raises:
            ValueError: If the identifier is empty or invalid.
            APIError: If there is an error response from the API.

        Example:
            >>> segments_details = await client.people.contacts.egments.list(identifier="XXX")

        Note:
            This method is a coroutine and must be called using await.
        """

        return await self._client._request("GET", self.root_path + "/" + identifier + "/segments", headers=self.headers)