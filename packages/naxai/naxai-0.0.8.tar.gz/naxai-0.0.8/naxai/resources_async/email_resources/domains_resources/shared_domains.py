class SharedDomainsResource:
    """ shared_domains resource for email.domains resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/shared-domains"
        self.headers = {"Content-Type": "application/json"}
            
    async def list(self):
        """
        Retrieves a list of shared domains.

        Returns:
            dict: The API response containing the list of shared domains.

        Example:
            >>> response = await client.email.domains.shared_domains.list()
        """
        self._client.logger.debug("shared-domains url: %s", self.root_path)
        return await self._client._request("GET", self.root_path, headers=self.headers)