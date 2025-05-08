from typing import Optional
from pydantic import Field, validate_call
from .domains_resources.shared_domains import SharedDomainsResource

class DomainsResource:
    """ domains resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/domains"
        self.headers = {"Content-Type": "application/json"}
        self.shared_domains = SharedDomainsResource(client, self.root_path)

    async def update_tracking_settings(self,
                                       domain_id: str,
                                       enabled: Optional[bool] = None):
        """
         Updates the tracking settings for a domain.

         Args:
            domain_id (str): The ID of the domain to update.
            enabled (bool, optional): Whether to enable or disable tracking. Defaults to None.

         Returns:
            dict: The API response indicating the success of the update.

         Example:
            >>> response = await client.email.domains.update_tracking_settings(domain_id="example.com", enabled=True)
         """
        return await self._client._request("PUT", self.root_path + "/" + domain_id + "/tracking/activities", json={"enabled": enabled} if enabled is not None else None, headers=self.headers)


    async def update_tracking_cname(self,
                                    domain_id:str,
                                    prefix: Optional[str] = "track"):
        """
        Updates the tracking CNAME for a domain.

        Args:
            domain_id (str): The ID of the domain to update.

        Returns:
            dict: The API response indicating the success of the update.

        Example:
            >>> response = await client.email.domains.update_tracking_cname(domain_id="example.com")
        """
        return await self._client._request("PUT", self.root_path + "/" + domain_id + "/tracking/prefix", json={"prefix": prefix}, headers=self.headers)

    async def verify(self, domain_id:str):
         """
         Verifies the DNS records for a domain.

         Args:
            domain_id (str): The ID of the domain to verifiy

        Returns:
            dict: The API response indicating the verification results of the domain.

        Example:
            >>> response = await client.email.domains.verify(domain_id="example.com")
         """
         return await self._client._request("GET", self.root_path + "/" + domain_id + "/verify", headers=self.headers)

    async def delete(self, domain_id:str):
        """
        Deletes a domain.

        Args:
            domain_id (str): The ID of the domain to delete.

        Returns:
            dict: The API response indicating the success of the deletion.

        Example:
            >>> response = await client.email.domains.delete(domain_id="example.com")
        """
        return await self._client._request("DELETE", self.root_path + "/" + domain_id, headers=self.headers)

    #TODO: get explanations
    async def update(self, domain_id:str):
            """
            Updates a domain.

            Args:
                domain_id (str): The ID of the domain to update.

            Returns:
                dict: The API response containing the updated domain.

            Example:
                >>> response = await client.email.domains.update(domain_id="example.com")
            """
            return await self._client._request("PUT", self.root_path + "/" + domain_id, headers=self.headers)

    async def get(self, domain_id: str):
        """
        Retrieves a specific domain.

        Args:
            domain_id (str): The ID of the domain to retrieve.

        Returns:
            dict: The API response containing the domain details.

        Example:
            >>> response = await client.email.domains.get(domain_id="example.com")
        """
        self._client.logger.debug("domains url: %s", self.root_path)
        return await self._client._request("GET", self.root_path + "/" + domain_id, headers=self.headers)
    
    @validate_call
    async def create(self,
                     domain_name: str = Field(min_length=3),
                     shared_with_subaccounts: Optional[bool] = False):
        """
        Creates a new domain.

        Args:
            domain_name (str): The name of the domain to create.
            shared_with_subaccounts (bool, optional): Whether the domain should be shared with subaccounts. Defaults to False.

        Returns:
            dict: The API response containing the created domain.

        Example:
            >>> response = await client.email.domains.create(domain_name="example.com")
        """
        data = {
            "domainName": domain_name,
            "sharedWithSubaccounts": shared_with_subaccounts
        }

        return await self._client._request("POST", self.root_path, json=data, headers=self.headers)

    async def list(self):
        """
        Retrieves a list of domains.

        Returns:
            dict: The API response containing the list of domains.

        Example:
            >>> response = await client.email.domains.list()
        """
        return await self._client._request("GET", self.root_path, headers=self.headers)