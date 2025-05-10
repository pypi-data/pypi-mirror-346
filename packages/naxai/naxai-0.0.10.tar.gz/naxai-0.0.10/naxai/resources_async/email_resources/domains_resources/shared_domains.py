import json
from naxai.models.email.responses.domains_responses import ListSharedDomainsResponse

class SharedDomainsResource:
    """ shared_domains resource for email.domains resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/shared-domains"
        self.headers = {"Content-Type": "application/json"}

    async def list(self):
        """
        Retrieve a list of shared domains available in the Naxai email system.
        
        This method fetches all shared domains that are available for use in your account.
        Shared domains are domains that have been pre-configured and verified by Naxai
        or your organization administrators, allowing you to send emails from these domains
        without having to verify your own domain.
        
        Returns:
            ListSharedDomainsResponse: A response object containing a list of shared domains.
            Each domain in the list includes:
                - id (str): Unique identifier for the shared domain
                - domain_name (str): The fully qualified domain name (e.g., "shared.example.com")
                - Additional metadata may be included depending on the API version
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access shared domains
        
        Example:
            >>> # Fetch all available shared domains
            >>> shared_domains = await client.email.domains.shared_domains.list()
            >>> print(f"Found {len(shared_domains)} shared domains:")
            >>> for domain in shared_domains:
            ...     print(f"- {domain.domain_name} (ID: {domain.id})")
            Found 3 shared domains:
            - shared1.naxai.com (ID: dom_123abc)
            - shared2.naxai.com (ID: dom_456def)
            - marketing.naxai.com (ID: dom_789ghi)
            
            >>> # Check if a specific shared domain is available
            >>> domain_to_find = "marketing.naxai.com"
            >>> available_domains = [d.domain_name for d in shared_domains]
            >>> if domain_to_find in available_domains:
            ...     print(f"{domain_to_find} is available for use")
            ... else:
            ...     print(f"{domain_to_find} is not available")
            marketing.naxai.com is available for use
        
        Note:
            - Shared domains are already verified and configured for proper email delivery
            - Using shared domains can be convenient but may have limitations compared to custom domains
            - Shared domains are typically used for testing or when custom domain verification is not possible
            - The response is a list-like object that supports iteration, indexing, and len() operations
            - No parameters are required for this method as it returns all available shared domains
            - The method logs the API request URL at debug level for troubleshooting purposes
        
        See Also:
            ListSharedDomainsResponse: For the structure of the response object
            DomainsResource.list: For retrieving custom domains owned by your account
        """
        return ListSharedDomainsResponse.model_validate_json(json.dumps(await self._client._request("GET", self.root_path, headers=self.headers)))