import json
from typing import Optional
from pydantic import Field, validate_call
from .domains_resources.shared_domains import SharedDomainsResource
from naxai.models.email.responses.domains_responses import (VerifyDomainResponse,
                                                            UpdateDomainResponse,
                                                            GetDomainResponse,
                                                            ListDomainsResponse,
                                                            CreateDomainResponse)
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
         SHOULD NOT BE USED. DOESNT RETURN A MODEL
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
        SHOULD NOT BE USED. DOESNT RETURN A MODEL
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
        Verify the DNS configuration of a domain in the Naxai email system.
        
        This method checks the DNS records for a domain to verify that they are correctly
        configured for email sending, including SPF, DKIM, tracking, MX, and ownership verification.
        It helps diagnose configuration issues and confirms when a domain is properly set up.
        
        Args:
            domain_id (str): Unique identifier of the domain to verify.
                This can be obtained from the create() or list() methods.
        
        Returns:
            VerifyDomainResponse: A response object containing verification status for each required DNS record:
                - spf_record: Status of the SPF record configuration
                    - current_value: The current SPF record value found in DNS
                    - verified: Whether the SPF record is correctly configured
                - dkim_record: Status of the DKIM record configuration
                    - current_value: The current DKIM record value found in DNS
                    - verified: Whether the DKIM record is correctly configured
                - tracking_record: Status of the tracking CNAME record configuration
                    - current_value: The current tracking record value found in DNS
                    - verified: Whether the tracking record is correctly configured
                - mx_record: Status of the MX record configuration
                    - current_value: The current MX record value found in DNS
                    - verified: Whether the MX record is correctly configured
                - verification_token: Status of the domain ownership verification token
                    - current_value: The current verification token found in DNS
                    - verified: Whether the verification token is correctly configured
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to verify domains
            NaxaiResourceNotFound: If the specified domain_id doesn't exist
        
        Example:
            >>> # Verify a domain's DNS configuration
            >>> verification = await client.email.domains.verify(domain_id="dom_123abc")
            >>> 
            >>> # Check overall verification status
            >>> all_verified = all([
            ...     verification.spf_record.verified,
            ...     verification.dkim_record.verified,
            ...     verification.tracking_record.verified,
            ...     verification.mx_record.verified,
            ...     verification.verification_token.verified
            ... ])
            >>> print(f"Domain fully verified: {all_verified}")
            >>> 
            >>> # Check which records need attention
            >>> if not verification.spf_record.verified:
            ...     print("SPF record needs to be configured")
            ...     print(f"Current value: {verification.spf_record.current_value or 'Not found'}")
            >>> 
            >>> if not verification.dkim_record.verified:
            ...     print("DKIM record needs to be configured")
            ...     print(f"Current value: {verification.dkim_record.current_value or 'Not found'}")
            >>> 
            >>> if not verification.tracking_record.verified:
            ...     print("Tracking record needs to be configured")
            ...     print(f"Current value: {verification.tracking_record.current_value or 'Not found'}")
            >>> 
            >>> if not verification.mx_record.verified:
            ...     print("MX record needs to be configured")
            ...     print(f"Current value: {verification.mx_record.current_value or 'Not found'}")
            >>> 
            >>> if not verification.verification_token.verified:
            ...     print("Verification token needs to be configured")
            ...     print(f"Current value: {verification.verification_token.current_value or 'Not found'}")
            Domain fully verified: False
            SPF record needs to be configured
            Current value: Not found
            DKIM record needs to be configured
            Current value: Not found
        
        Note:
            - This method performs a real-time check of the domain's DNS records
            - DNS propagation can take time (up to 24-48 hours), so records may not verify immediately
            - All records must be verified for the domain to be fully functional for email sending
            - The required DNS records include:
            * SPF (Sender Policy Framework): Helps prevent email spoofing
            * DKIM (DomainKeys Identified Mail): Provides email authentication
            * Tracking record: Enables open and click tracking
            * MX record: Configures mail exchange servers
            * Verification token: Proves domain ownership
            - The current_value field shows what was found in DNS, which helps diagnose issues
            - If a record is not verified, you may need to:
            1. Check that you've added the correct record to your DNS
            2. Wait for DNS propagation to complete
            3. Ensure there are no conflicting records
            - Use the get() method to retrieve the expected values for each DNS record
        
        See Also:
            get: For retrieving the expected DNS record values for a domain
            create: For creating a new domain
            list: For retrieving all domains in your account
            VerifyDomainResponse: For the structure of the verification response
            BaseRecord: For the structure of individual record verification status
        """
        return VerifyDomainResponse.model_validate_json(json.dumps(await self._client._request("GET", self.root_path + "/" + domain_id + "/verify", headers=self.headers)))

    async def delete(self, domain_id:str):
        """
        Delete a domain from the Naxai email system.
        
        This method permanently removes a domain from your account. Once deleted,
        you will no longer be able to send emails from this domain unless you add it again.
        
        Args:
            domain_id (str): Unique identifier of the domain to delete.
                This can be obtained from the create() or list() methods.
        
        Returns:
            None: The API returns a 204 No Content response on successful deletion.
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to delete domains
            NaxaiResourceNotFound: If the specified domain_id doesn't exist
        
        Example:
            >>> # Delete a domain that is no longer needed
            >>> await client.email.domains.delete(domain_id="dom_123abc")
            >>> print("Domain successfully deleted")
            Domain successfully deleted
            
            >>> # Verify the domain is no longer in the list
            >>> domains = await client.email.domains.list()
            >>> domain_ids = [domain.id for domain in domains]
            >>> if "dom_123abc" not in domain_ids:
            ...     print("Domain has been removed from the account")
            Domain has been removed from the account
        
        Note:
            - This operation cannot be undone
            - If you delete a domain that is actively being used for sending emails, those emails may fail
            - Any sender identities associated with this domain will also be invalidated
            - If you want to use the domain again in the future, you'll need to add it again
            and go through the verification process
            - Consider using the get() method before deletion to ensure you're deleting the correct domain
        
        See Also:
            list: For retrieving all domains in your account
            get: For retrieving details about a specific domain
            create: For adding a new domain to your account
        """
        return await self._client._request("DELETE", self.root_path + "/" + domain_id, headers=self.headers)

    #TODO: get explanations
    async def update(self, domain_id:str):
        """
        Update a domain's configuration in the Naxai email system.
        
        This method refreshes a domain's configuration and checks its verification status.
        It can be used to update the system's information about a domain after DNS changes
        have been made or to refresh the verification status.
        
        Args:
            domain_id (str): Unique identifier of the domain to update.
                This can be obtained from the create() or list() methods.
        
        Returns:
            UpdateDomainResponse: A response object containing the updated domain information:
                - id: Unique identifier for the domain
                - domain_name: The fully qualified domain name
                - shared_with_subaccounts: Whether this domain is shared with subaccounts
                - verification_token: Token used for domain ownership verification
                - dkim_name: The DNS record name for DKIM authentication
                - dkim_value: The DNS record value for DKIM authentication
                - spf_record: The recommended SPF record for the domain
                - verified: Whether the domain has been verified as owned by the account
                - tracking_name: The DNS record name for email tracking configuration
                - tracking_enabled: Whether email tracking is enabled for this domain
                - tracking_validated: Whether the tracking DNS records have been validated
                - tracking_record: The DNS record value for email tracking configuration
                - modified_at: Timestamp when the domain was last modified
                - modified_by: Identifier of the user who last modified the domain
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to update domains
            NaxaiResourceNotFound: If the specified domain_id doesn't exist
        
        Example:
            >>> # Update a domain after making DNS changes
            >>> updated_domain = await client.email.domains.update(domain_id="dom_123abc")
            >>> 
            >>> print(f"Domain: {updated_domain.domain_name}")
            >>> print(f"Verification status: {'Verified' if updated_domain.verified else 'Not verified'}")
            >>> print(f"Tracking enabled: {updated_domain.tracking_enabled}")
            >>> print(f"Tracking validated: {updated_domain.tracking_validated}")
            >>> print(f"Last modified: {updated_domain.modified_at}")
            Domain: example.com
            Verification status: True
            Tracking enabled: True
            Tracking validated: True
            Last modified: 1703066500000
        
        Note:
            - This method is useful after making DNS changes to refresh the verification status
            - It does not currently support modifying domain properties (such as shared_with_subaccounts)
            - The response includes the current verification status of the domain
            - If the domain is not verified, use the verify() method to get detailed information
            about which DNS records need to be configured
            - The modified_at timestamp will be updated to reflect this operation
        
        TODO:
            - Add support for updating domain properties
        
        See Also:
            verify: For checking the DNS configuration of a domain
            get: For retrieving details about a specific domain without updating
            UpdateDomainResponse: For the structure of the update response
        """
        return UpdateDomainResponse.model_validate_json(json.dumps(await self._client._request("PUT", self.root_path + "/" + domain_id, headers=self.headers)))

    async def get(self, domain_id: str):
        """
        Retrieve detailed information about a specific domain in the Naxai email system.
        
        This method fetches comprehensive information about a domain, including its
        verification status, DNS configuration details, and tracking settings. It provides
        all the information needed to configure and manage the domain for email sending.
        
        Args:
            domain_id (str): Unique identifier of the domain to retrieve.
                This can be obtained from the create() or list() methods.
        
        Returns:
            GetDomainResponse: A response object containing detailed domain information:
                - id: Unique identifier for the domain
                - domain_name: The fully qualified domain name
                - shared_with_subaccounts: Whether this domain is shared with subaccounts
                - verification_token: Token used for domain ownership verification
                - dkim_name: The DNS record name for DKIM authentication
                - dkim_value: The DNS record value for DKIM authentication
                - spf_record: The recommended SPF record for the domain
                - verified: Whether the domain has been verified as owned by the account
                - tracking_name: The DNS record name for email tracking configuration
                - tracking_enabled: Whether email tracking is enabled for this domain
                - tracking_validated: Whether the tracking DNS records have been validated
                - tracking_record: The DNS record value for email tracking configuration
                - modified_at: Timestamp when the domain was last modified
                - modified_by: Identifier of the user who last modified the domain
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access domain information
            NaxaiResourceNotFound: If the specified domain_id doesn't exist
        
        Example:
            >>> # Retrieve domain details
            >>> domain = await client.email.domains.get(domain_id="dom_123abc")
            >>> 
            >>> print(f"Domain: {domain.domain_name} (ID: {domain.id})")
            >>> print(f"Verification status: {'Verified' if domain.verified else 'Not verified'}")
            >>> 
            >>> # Display DNS configuration information
            >>> if not domain.verified:
            ...     print("\nDNS Configuration Required:")
            ...     print(f"Verification token: Add TXT record with value: {domain.verification_token}")
            ...     print(f"DKIM: Add {domain.dkim_name} with value: {domain.dkim_value}")
            ...     print(f"SPF: Add or update TXT record with: {domain.spf_record}")
            >>> 
            >>> # Display tracking configuration
            >>> print(f"\nTracking enabled: {domain.tracking_enabled}")
            >>> print(f"Tracking validated: {domain.tracking_validated}")
            >>> if domain.tracking_enabled and not domain.tracking_validated:
            ...     print(f"Add CNAME record {domain.tracking_name} with value: {domain.tracking_record}")
            Domain: example.com (ID: dom_123abc)
            Verification status: False
            
            DNS Configuration Required:
            Verification token: Add TXT record with value: naxai-verification=abc123def456
            DKIM: Add dkim._domainkey.example.com with value: v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...
            SPF: Add or update TXT record with: v=spf1 include:spf.naxai.com ~all
            
            Tracking enabled: True
            Tracking validated: False
            Add CNAME record track.example.com with value: track.naxai.com
        
        Note:
            - This method retrieves the current state of the domain without making any changes
            - The response includes all the DNS records that need to be configured for the domain
            - For domain ownership verification, add a TXT record with the verification_token value
            - For DKIM authentication, add a TXT record at dkim_name with the dkim_value
            - For SPF configuration, add or update a TXT record with the spf_record value
            - For tracking configuration, add a CNAME record at tracking_name with the tracking_record value
            - The verified field indicates whether the domain ownership has been verified
            - The tracking_validated field indicates whether the tracking configuration has been verified
            - Use the verify() method to check the current DNS configuration status
        
        See Also:
            verify: For checking the DNS configuration of a domain
            create: For adding a new domain to your account
            list: For retrieving all domains in your account
            GetDomainResponse: For the structure of the domain response
        """
        return GetDomainResponse.model_validate_json(json.dumps(await self._client._request("GET", self.root_path + "/" + domain_id, headers=self.headers)))

    @validate_call
    async def create(self,
                     domain_name: str = Field(min_length=3),
                     shared_with_subaccounts: Optional[bool] = False):
        """
        Add a new domain to the Naxai email system.
        
        This method registers a domain with your account, allowing you to send emails
        from addresses at that domain once it's verified. It generates the necessary
        DNS records that need to be configured for domain verification, DKIM authentication,
        SPF, and tracking.
        
        Args:
            domain_name (str): The fully qualified domain name to add (e.g., "example.com").
                Must be at least 3 characters long.
            shared_with_subaccounts (Optional[bool]): Whether this domain should be shared with
                subaccounts, allowing them to send emails from this domain. Defaults to False.
        
        Returns:
            CreateDomainResponse: A response object containing the newly created domain information:
                - id: Unique identifier for the domain
                - domain_name: The fully qualified domain name
                - shared_with_subaccounts: Whether this domain is shared with subaccounts
                - verification_token: Token used for domain ownership verification
                - dkim_name: The DNS record name for DKIM authentication
                - dkim_value: The DNS record value for DKIM authentication
                - spf_record: The recommended SPF record for the domain
                - verified: Whether the domain has been verified (typically False for new domains)
                - tracking_name: The DNS record name for email tracking configuration
                - tracking_enabled: Whether email tracking is enabled for this domain
                - tracking_validated: Whether the tracking DNS records have been validated
                - tracking_record: The DNS record value for email tracking configuration
                - modified_at: Timestamp when the domain was created
                - modified_by: Identifier of the user who created the domain
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to create domains
            ValidationError: If the domain_name is less than 3 characters
        
        Example:
            >>> # Add a new domain to your account
            >>> new_domain = await client.email.domains.create(
            ...     domain_name="example.com",
            ...     shared_with_subaccounts=True
            ... )
            >>> 
            >>> print(f"Domain created: {new_domain.domain_name} (ID: {new_domain.id})")
            >>> print(f"Shared with subaccounts: {new_domain.shared_with_subaccounts}")
            >>> 
            >>> # Display DNS configuration instructions
            >>> print("\nDNS Configuration Required:")
            >>> print(f"1. Verification token: Add TXT record with value: {new_domain.verification_token}")
            >>> print(f"2. DKIM: Add {new_domain.dkim_name} with value: {new_domain.dkim_value}")
            >>> print(f"3. SPF: Add or update TXT record with: {new_domain.spf_record}")
            >>> print(f"4. Tracking: Add CNAME record {new_domain.tracking_name} with value: {new_domain.tracking_record}")
            >>> 
            >>> # After configuring DNS, verify the domain
            >>> print("\nAfter configuring DNS records, verify the domain:")
            >>> print(f"await client.email.domains.verify(domain_id=\"{new_domain.id}\")")
            Domain created: example.com (ID: dom_123abc)
            Shared with subaccounts: True
            
            DNS Configuration Required:
            1. Verification token: Add TXT record with value: naxai-verification=abc123def456
            2. DKIM: Add dkim._domainkey.example.com with value: v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...
            3. SPF: Add or update TXT record with: v=spf1 include:spf.naxai.com ~all
            4. Tracking: Add CNAME record track.example.com with value: track.naxai.com
            
            After configuring DNS records, verify the domain:
            await client.email.domains.verify(domain_id="dom_123abc")
        
        Note:
            - After creating a domain, you must configure DNS records to verify ownership and enable features
            - The domain will not be usable for sending emails until it's verified
            - DNS propagation can take time (up to 24-48 hours), so verification may not succeed immediately
            - The required DNS records include:
            * TXT record for domain ownership verification
            * TXT record for DKIM authentication
            * TXT record for SPF configuration
            * CNAME record for tracking configuration
            - The shared_with_subaccounts parameter determines whether subaccounts can use this domain
            - Once the domain is verified, you can create sender identities using this domain
            - Use the verify() method to check if your DNS configuration is correct
        
        See Also:
            verify: For checking the DNS configuration of a domain
            get: For retrieving details about a specific domain
            list: For retrieving all domains in your account
            CreateDomainResponse: For the structure of the creation response
        """
        data = {
            "domainName": domain_name,
            "sharedWithSubaccounts": shared_with_subaccounts
        }

        return CreateDomainResponse.model_validate_json(json.dumps(await self._client._request("POST", self.root_path, json=data, headers=self.headers)))

    async def list(self):
        """
        Retrieve a list of all domains registered in your Naxai email system account.
        
        This method fetches all domains that have been added to your account, including
        both verified and unverified domains. It provides an overview of all domains
        and their current verification status.
        
        Returns:
            ListDomainsResponse: A response object containing a list of domains.
            The response behaves like a list and includes:
                - root: List of domain objects, each containing:
                    - id: Unique identifier for the domain
                    - domain_name: The fully qualified domain name
                    - shared_with_subaccounts: Whether this domain is shared with subaccounts
                    - verification_token: Token used for domain ownership verification
                    - dkim_name: The DNS record name for DKIM authentication
                    - dkim_value: The DNS record value for DKIM authentication
                    - spf_record: The recommended SPF record for the domain
                    - verified: Whether the domain has been verified as owned by the account
                    - tracking_name: The DNS record name for email tracking configuration
                    - tracking_enabled: Whether email tracking is enabled for this domain
                    - tracking_validated: Whether the tracking DNS records have been validated
                    - tracking_record: The DNS record value for email tracking configuration
                    - modified_at: Timestamp when the domain was last modified
                    - modified_by: Identifier of the user who last modified the domain
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to list domains
        
        Example:
            >>> # Retrieve all domains in your account
            >>> domains = await client.email.domains.list()
            >>> 
            >>> print(f"Found {len(domains)} domains:")
            >>> for domain in domains:
            ...     status = "✓ Verified" if domain.verified else "✗ Not verified"
            ...     print(f"- {domain.domain_name} ({status})")
            Found 3 domains:
            - example.com (✓ Verified)
            - marketing.example.com (✓ Verified)
            - new-domain.example.com (✗ Not verified)
            
            >>> # Find domains that need verification
            >>> unverified = [d for d in domains if not d.verified]
            >>> if unverified:
            ...     print("\nDomains requiring verification:")
            ...     for domain in unverified:
            ...         print(f"- {domain.domain_name} (ID: {domain.id})")
            ...         print(f"  Verification token: {domain.verification_token}")
            Domains requiring verification:
            - new-domain.example.com (ID: dom_789ghi)
            Verification token: naxai-verification=xyz789abc
            
            >>> # Find domains with tracking issues
            >>> tracking_issues = [d for d in domains if d.tracking_enabled and not d.tracking_validated]
            >>> if tracking_issues:
            ...     print("\nDomains with tracking configuration issues:")
            ...     for domain in tracking_issues:
            ...         print(f"- {domain.domain_name}")
            ...         print(f"  Add CNAME record {domain.tracking_name} with value: {domain.tracking_record}")
            Domains with tracking configuration issues:
            - new-domain.example.com
            Add CNAME record track.new-domain.example.com with value: track.naxai.com
        
        Note:
            - This method returns all domains associated with your account
            - The response is a list-like object that supports iteration, indexing, and len() operations
            - Each domain in the list includes its verification status and DNS configuration details
            - For domains that are not verified, you can use the verification_token, dkim_name,
            dkim_value, and spf_record fields to configure the necessary DNS records
            - For domains with tracking enabled but not validated, you can use the tracking_name
            and tracking_record fields to configure the necessary CNAME record
            - Use the verify() method to check the DNS configuration status of specific domains
            - Use the get() method to retrieve detailed information about a specific domain
        
        See Also:
            get: For retrieving detailed information about a specific domain
            create: For adding a new domain to your account
            verify: For checking the DNS configuration of a domain
            ListDomainsResponse: For the structure of the response object
        """
        return ListDomainsResponse.model_validate_json(json.dumps(await self._client._request("GET", self.root_path, headers=self.headers)))