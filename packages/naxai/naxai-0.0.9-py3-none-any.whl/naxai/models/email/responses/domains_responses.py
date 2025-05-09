from typing import List, Optional
from pydantic import BaseModel, Field

class BaseDomainResponse(BaseModel):
    """
    Base model representing domain information in the Naxai email system.
    
    This class defines the core structure for domain data, providing essential
    identification and naming information. It serves as the foundation for more
    specialized domain response models.
    
    Attributes:
        id (str): Unique identifier for the domain.
        domain_name (str): The fully qualified domain name (e.g., "example.com").
            Mapped from JSON key 'domainName'.
    
    Example:
        >>> domain = BaseDomainResponse(
        ...     id="dom_123abc",
        ...     domainName="example.com"
        ... )
        >>> print(f"Domain: {domain.domain_name} (ID: {domain.id})")
        Domain: example.com (ID: dom_123abc)
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - It serves as a base class for more specialized domain response models
        - Domain names are typically fully qualified domain names without protocols (e.g., "example.com", not "https://example.com")
    """
    id: str
    domain_name: str = Field(alias="domainName")

    model_config = {"populate_by_name": True}

class ExtendedDomainResponse(BaseDomainResponse):
    """
    Base model for domain responses with extended configuration details in the Naxai email system.
    
    This class extends BaseDomainResponse to include comprehensive information about
    a domain's verification status, DNS records, tracking configuration, and sharing settings.
    It serves as a common base for more specific domain response types that include
    detailed configuration information.
    
    Attributes:
        id (str): Unique identifier for the domain (inherited from BaseDomainResponse).
        domain_name (str): The fully qualified domain name (inherited from BaseDomainResponse).
        shared_with_subaccounts (bool): Whether this domain is shared with subaccounts.
            Mapped from JSON key 'sharedWithSubaccounts'.
        verification_token (str): Token used for domain ownership verification.
            Mapped from JSON key 'verificationToken'.
        dkim_name (str): The DNS record name for DKIM authentication.
            Mapped from JSON key 'dkimName'.
        dkim_value (str): The DNS record value for DKIM authentication.
            Mapped from JSON key 'dkimValue'.
        spf_record (str): The recommended SPF record for the domain.
            Mapped from JSON key 'spfRecord'.
        verified (bool): Whether the domain has been verified as owned by the account.
            Mapped from JSON key 'verified'.
        tracking_name (str): The DNS record name for email tracking configuration.
            Mapped from JSON key 'trackingName'.
        tracking_enabled (bool): Whether email tracking is enabled for this domain.
            Mapped from JSON key 'trackingEnabled'.
        tracking_validated (bool): Whether the tracking DNS records have been validated.
            Mapped from JSON key 'trackingValidated'.
        tracking_record (str): The DNS record value for email tracking configuration.
            Mapped from JSON key 'trackingRecord'.
        modified_at (int): Timestamp when the domain was last modified, in milliseconds since epoch.
            Mapped from JSON key 'modifiedAt'.
        modified_by (str): Identifier of the user who last modified the domain.
            Mapped from JSON key 'modifiedBy'.
    
    Example:
        >>> domain = ExtendedDomainResponse(
        ...     id="dom_123abc",
        ...     domainName="example.com",
        ...     sharedWithSubaccounts=True,
        ...     verificationToken="verify_token_xyz",
        ...     dkimName="_dkim.example.com",
        ...     dkimValue="v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
        ...     spfRecord="v=spf1 include:spf.naxai.com ~all",
        ...     verified=True,
        ...     trackingName="track.example.com",
        ...     trackingEnabled=True,
        ...     trackingValidated=True,
        ...     trackingRecord="CNAME track.naxai.com",
        ...     modifiedAt=1703066400000,
        ...     modifiedBy="usr_789xyz"
        ... )
        >>> print(f"Domain: {domain.domain_name} (Verified: {domain.verified})")
        >>> print(f"DKIM: {domain.dkim_name} = {domain.dkim_value}")
        >>> print(f"SPF: {domain.spf_record}")
    
    Note:
        - This class serves as a base for more specific domain response types like
          ListDomainsResponse and CreateDomainResponse
        - All fields except id, domain_name, and shared_with_subaccounts may be None if not provided
        - The verification_token is used to create a DNS TXT record to prove domain ownership
        - DKIM and SPF records are used for email authentication and deliverability
        - Tracking configuration enables open and click tracking for emails sent from this domain
        - The modified_at timestamp is in milliseconds since epoch
    
    See Also:
        BaseDomainResponse: For the base domain information structure
        ListDomainsResponse: For responses when listing domains
        CreateDomainResponse: For responses when creating new domains
    """
    shared_with_subaccounts: Optional[bool] = Field(alias="sharedWithSubaccounts", default=None)
    verification_token: str = Field(alias="verificationToken", default=None)
    dkim_name: str = Field(alias="dkimName", default=None)
    dkim_value: str = Field(alias="dkimValue", default=None)
    spf_record: str = Field(alias="spfRecord", default=None)
    verified: bool = Field(alias="verified", default=None)
    tracking_name: str = Field(alias="trackingName", default=None)
    tracking_enabled: bool = Field(alias="trackingEnabled", default=None)
    tracking_validated: bool = Field(alias="trackingValidated", default=None)
    tracking_record: str = Field(alias="trackingRecord", default=None)
    modified_at: int = Field(alias="modifiedAt", default=None)
    modified_by: str = Field(alias="modifiedBy", default=None)

class ListSharedDomainsResponse(BaseModel):
    """
    Model representing a shared domain in the Naxai email system.
    
    This class extends BaseDomainResponse to represent domains that are shared
    across multiple users or organizations within the system.
    
    Inherits all attributes from BaseDomainResponse:
        - id (str): Unique identifier for the domain
        - domain_name (str): The fully qualified domain name
    
    Example:
        >>> shared_domain = ListSharedDomains(
        ...     id="dom_123abc",
        ...     domainName="shared.example.com"
        ... )
        >>> print(f"Shared domain: {shared_domain.domain_name}")
        Shared domain: shared.example.com
    
    Note:
        - Shared domains can be used by multiple users or organizations
        - This model is typically used in responses listing available shared domains
    
    See Also:
        BaseDomainResponse: For the base domain information structure
    """
    root: List[BaseDomainResponse] = Field(default_factory=list)
    
    def __len__(self) -> int:
        """Return the number of domains in the list."""
        return len(self.root)
    
    def __getitem__(self, index):
        """Access domains by index."""
        return self.root[index]
    
    def __iter__(self):
        """Iterate through domains."""
        return iter(self.root)
    
    @classmethod
    def model_validate_json(cls, json_data: str, **kwargs):
        """Parse JSON data into the model.
        
        This method handles both array-style JSON and object-style JSON with a root field.
        
        Args:
            json_data (str): The JSON string to parse
            **kwargs: Additional arguments to pass to the standard model_validate_json method
            
        Returns:
            ListDomainsResponse: A validated instance of the class
        """
        import json
        data = json.loads(json_data)
        
        # If the data is a list, wrap it in a dict with the root field
        if isinstance(data, list):
            return cls(root=data)
        
        # Otherwise, use the standard Pydantic validation
        return super().model_validate_json(json_data, **kwargs)

class ListDomainsResponse(BaseModel):
    """
    Model representing a list of domains with detailed configuration in the Naxai email system.
    
    This class behaves like a list of ExtendedDomainResponse objects while maintaining
    Pydantic validation capabilities. It can parse JSON responses that contain either
    a direct array of domains or an object with a root field containing domains.
    
    Attributes:
        root (list[ExtendedDomainResponse]): List of domain objects with detailed configuration.
    
    Example:
        >>> # Creating from a list of domains
        >>> domains_list = ListDomainsResponse(
        ...     root=[
        ...         ExtendedDomainResponse(
        ...             id="dom_123abc",
        ...             domainName="example.com",
        ...             sharedWithSubaccounts=True,
        ...             verified=True
        ...         ),
        ...         ExtendedDomainResponse(
        ...             id="dom_456def",
        ...             domainName="another-example.com",
        ...             sharedWithSubaccounts=False,
        ...             verified=False
        ...         )
        ...     ]
        ... )
        >>> print(f"Found {len(domains_list)} domains")
        >>> for domain in domains_list:
        ...     print(f"Domain: {domain.domain_name} (Verified: {domain.verified})")
        >>> 
        >>> # Parsing from JSON with a direct array
        >>> json_array = '[{"id": "dom_123", "domainName": "example.com", "sharedWithSubaccounts": true}]'
        >>> parsed = ListDomainsResponse.model_validate_json(json_array)
        >>> 
        >>> # Parsing from JSON with a root element
        >>> json_data = '{"root": [{"id": "dom_123", "domainName": "example.com", "sharedWithSubaccounts": true}]}'
        >>> parsed = ListDomainsResponse.model_validate_json(json_data)
    
    Note:
        - This class behaves like a list, supporting iteration, indexing, and len()
        - It can parse both direct JSON arrays and JSON objects with a 'root' field
        - All domains in the list are ExtendedDomainResponse objects with full configuration details
    """
    root: List[ExtendedDomainResponse] = Field(default_factory=list)
    
    def __len__(self) -> int:
        """Return the number of domains in the list."""
        return len(self.root)
    
    def __getitem__(self, index):
        """Access domains by index."""
        return self.root[index]
    
    def __iter__(self):
        """Iterate through domains."""
        return iter(self.root)
    
    @classmethod
    def model_validate_json(cls, json_data: str, **kwargs):
        """Parse JSON data into the model.
        
        This method handles both array-style JSON and object-style JSON with a root field.
        
        Args:
            json_data (str): The JSON string to parse
            **kwargs: Additional arguments to pass to the standard model_validate_json method
            
        Returns:
            ListDomainsResponse: A validated instance of the class
        """
        import json
        data = json.loads(json_data)
        
        # If the data is a list, wrap it in a dict with the root field
        if isinstance(data, list):
            return cls(root=data)
        
        # Otherwise, use the standard Pydantic validation
        return super().model_validate_json(json_data, **kwargs)

class CreateDomainResponse(ExtendedDomainResponse):
    """
    Model representing the response from creating a new domain in the Naxai email system.
    
    This class extends ExtendedDomainResponse to represent the API response when
    a new domain is successfully created. It includes all the configuration details
    needed for domain verification and setup.
    
    Inherits all attributes from ExtendedDomainResponse:
        - id (str): Unique identifier for the newly created domain
        - domain_name (str): The fully qualified domain name
        - shared_with_subaccounts (bool): Whether this domain is shared with subaccounts
        - verification_token (str): Token used for domain ownership verification
        - dkim_name (str): The DNS record name for DKIM authentication
        - dkim_value (str): The DNS record value for DKIM authentication
        - spf_record (str): The recommended SPF record for the domain
        - verified (bool): Whether the domain has been verified (typically false for new domains)
        - tracking_name (str): The DNS record name for email tracking configuration
        - tracking_enabled (bool): Whether email tracking is enabled for this domain
        - tracking_validated (bool): Whether the tracking DNS records have been validated
        - tracking_record (str): The DNS record value for email tracking configuration
        - modified_at (int): Timestamp when the domain was created
        - modified_by (str): Identifier of the user who created the domain
    
    Example:
        >>> response = CreateDomainResponse(
        ...     id="dom_123abc",
        ...     domainName="example.com",
        ...     sharedWithSubaccounts=True,
        ...     verificationToken="verify_token_xyz",
        ...     dkimName="_dkim.example.com",
        ...     dkimValue="v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
        ...     spfRecord="v=spf1 include:spf.naxai.com ~all",
        ...     verified=False,
        ...     trackingName="track.example.com",
        ...     trackingEnabled=True,
        ...     trackingValidated=False,
        ...     trackingRecord="CNAME track.naxai.com",
        ...     modifiedAt=1703066400000,
        ...     modifiedBy="usr_789xyz"
        ... )
        >>> print(f"Domain {response.domain_name} created with ID: {response.id}")
        >>> print(f"To verify ownership, add this TXT record: {response.verification_token}")
        >>> print(f"Add DKIM record: {response.dkim_name} with value: {response.dkim_value}")
        >>> print(f"Recommended SPF record: {response.spf_record}")
    
    Note:
        - After domain creation, DNS records must be configured to verify ownership
        - The verification_token should be added as a TXT record at the domain's DNS settings
        - DKIM and SPF records should be configured to improve email deliverability
        - For tracking functionality, the tracking_record should be added as a CNAME record
        - Newly created domains typically have verified=False and tracking_validated=False
          until DNS records are properly configured and verified
        - The modified_at timestamp represents the creation time in milliseconds since epoch
    
    See Also:
        ExtendedDomainResponse: For the base structure of domain responses with configuration
        BaseDomainResponse: For the core domain information structure
    """

class GetDomainResponse(ExtendedDomainResponse):
    """
    Model representing the response from retrieving a specific domain in the Naxai email system.
    
    This class extends ExtendedDomainResponse to represent the API response when
    fetching detailed information about an existing domain. It includes comprehensive
    information about the domain's verification status, DNS configuration, and tracking settings.
    
    Inherits all attributes from ExtendedDomainResponse:
        - id (str): Unique identifier for the domain
        - domain_name (str): The fully qualified domain name
        - shared_with_subaccounts (bool): Whether this domain is shared with subaccounts
        - verification_token (str): Token used for domain ownership verification
        - dkim_name (str): The DNS record name for DKIM authentication
        - dkim_value (str): The DNS record value for DKIM authentication
        - spf_record (str): The recommended SPF record for the domain
        - verified (bool): Whether the domain has been verified as owned by the account
        - tracking_name (str): The DNS record name for email tracking configuration
        - tracking_enabled (bool): Whether email tracking is enabled for this domain
        - tracking_validated (bool): Whether the tracking DNS records have been validated
        - tracking_record (str): The DNS record value for email tracking configuration
        - modified_at (int): Timestamp when the domain was last modified
        - modified_by (str): Identifier of the user who last modified the domain
    
    Example:
        >>> response = GetDomainResponse(
        ...     id="dom_123abc",
        ...     domainName="example.com",
        ...     sharedWithSubaccounts=True,
        ...     verificationToken="verify_token_xyz",
        ...     dkimName="_dkim.example.com",
        ...     dkimValue="v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
        ...     spfRecord="v=spf1 include:spf.naxai.com ~all",
        ...     verified=True,
        ...     trackingName="track.example.com",
        ...     trackingEnabled=True,
        ...     trackingValidated=True,
        ...     trackingRecord="CNAME track.naxai.com",
        ...     modifiedAt=1703066400000,
        ...     modifiedBy="usr_789xyz"
        ... )
        >>> print(f"Domain: {response.domain_name} (ID: {response.id})")
        >>> print(f"Verification status: {'Verified' if response.verified else 'Not verified'}")
        >>> if not response.verified:
        ...     print(f"To verify, add TXT record with value: {response.verification_token}")
        >>> print(f"Tracking enabled: {response.tracking_enabled}")
        >>> print(f"Tracking validated: {response.tracking_validated}")
    
    Note:
        - This response provides the current state of a domain, including its verification status
        - If the domain is not verified (verified=False), the verification_token can be used
          to create the necessary DNS TXT record to prove ownership
        - The response includes all DNS records needed for proper email authentication and tracking
        - For domains with tracking enabled but not validated (tracking_enabled=True,
          tracking_validated=False), the tracking_record should be added as a CNAME record
        - The modified_at timestamp indicates when the domain was last updated
    
    See Also:
        ExtendedDomainResponse: For the base structure of domain responses with configuration
        CreateDomainResponse: For responses when creating new domains
        ListDomainsResponse: For responses when listing multiple domains
    """

class UpdateDomainResponse(ExtendedDomainResponse):
    """
    Model representing the response from updating a domain in the Naxai email system.
    
    This class extends ExtendedDomainResponse to represent the API response when
    modifying an existing domain's configuration. It includes the updated domain
    information reflecting the changes that were applied.
    
    Inherits all attributes from ExtendedDomainResponse:
        - id (str): Unique identifier for the domain
        - domain_name (str): The fully qualified domain name
        - shared_with_subaccounts (bool): Whether this domain is shared with subaccounts
        - verification_token (str): Token used for domain ownership verification
        - dkim_name (str): The DNS record name for DKIM authentication
        - dkim_value (str): The DNS record value for DKIM authentication
        - spf_record (str): The recommended SPF record for the domain
        - verified (bool): Whether the domain has been verified as owned by the account
        - tracking_name (str): The DNS record name for email tracking configuration
        - tracking_enabled (bool): Whether email tracking is enabled for this domain
        - tracking_validated (bool): Whether the tracking DNS records have been validated
        - tracking_record (str): The DNS record value for email tracking configuration
        - modified_at (int): Timestamp when the domain was last modified (updated with current time)
        - modified_by (str): Identifier of the user who performed this update
    
    Example:
        >>> response = UpdateDomainResponse(
        ...     id="dom_123abc",
        ...     domainName="example.com",
        ...     sharedWithSubaccounts=True,  # Updated value
        ...     verificationToken="verify_token_xyz",
        ...     dkimName="_dkim.example.com",
        ...     dkimValue="v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
        ...     spfRecord="v=spf1 include:spf.naxai.com ~all",
        ...     verified=True,
        ...     trackingName="track.example.com",
        ...     trackingEnabled=True,  # Updated value
        ...     trackingValidated=False,
        ...     trackingRecord="CNAME track.naxai.com",
        ...     modifiedAt=1703066400000,  # Updated with current timestamp
        ...     modifiedBy="usr_789xyz"  # Updated with current user
        ... )
        >>> print(f"Domain {response.domain_name} updated successfully")
        >>> print(f"Sharing with subaccounts: {response.shared_with_subaccounts}")
        >>> print(f"Tracking enabled: {response.tracking_enabled}")
        >>> print(f"Last modified: {response.modified_at} by {response.modified_by}")
        >>> if response.tracking_enabled and not response.tracking_validated:
        ...     print(f"Add tracking CNAME record: {response.tracking_name} = {response.tracking_record}")
    
    Note:
        - The response reflects the domain's state after the update operation
        - The modified_at field will contain the timestamp of this update operation
        - The modified_by field will identify the user who performed this update
        - If tracking settings were changed (tracking_enabled=True), but tracking is not yet
          validated (tracking_validated=False), the tracking_record should be added as a CNAME record
        - Changes to shared_with_subaccounts take effect immediately
        - The verification status (verified) is not affected by updates unless DNS records
          are changed, which may require re-verification
    
    See Also:
        ExtendedDomainResponse: For the base structure of domain responses with configuration
        GetDomainResponse: For retrieving the current state of a domain
        CreateDomainResponse: For responses when creating new domains
    """

class BaseRecord(BaseModel):
    """
    Base model representing a DNS record verification status in the Naxai email system.
    
    This class defines the structure for tracking the current value and verification status
    of DNS records associated with email domains. It is used as a component in domain
    verification responses to provide detailed information about each required DNS record.
    
    Attributes:
        current_value (str): The current value of the DNS record as detected by the system.
            This may be None if the record doesn't exist or couldn't be retrieved.
            Mapped from JSON key 'currentValue'.
        verified (bool): Whether the DNS record has been verified as correctly configured.
            This may be None if verification hasn't been attempted yet.
    
    Example:
        >>> record = BaseRecord(
        ...     currentValue="v=spf1 include:spf.naxai.com ~all",
        ...     verified=True
        ... )
        >>> print(f"Record value: {record.current_value}")
        >>> print(f"Verification status: {'Verified' if record.verified else 'Not verified'}")
        Record value: v=spf1 include:spf.naxai.com ~all
        Verification status: Verified
        
        >>> # Record that doesn't exist or hasn't been verified yet
        >>> missing_record = BaseRecord(
        ...     currentValue=None,
        ...     verified=False
        ... )
        >>> if missing_record.current_value is None:
        ...     print("Record not found")
        >>> if not missing_record.verified:
        ...     print("Record not verified")
        Record not found
        Record not verified
    
    Note:
        - This class is typically used as a component in domain verification responses
        - A verified=True status indicates that the record exists and matches the expected value
        - A verified=False status indicates that the record either doesn't exist or has an incorrect value
        - When current_value is None, it typically means the record couldn't be found in DNS
        - Different types of DNS records (SPF, DKIM, MX, etc.) use this same structure
          to report their verification status
    
    See Also:
        VerifyDomainResponse: For the complete domain verification response structure
    """
    current_value: str = Field(alias="currentValue", default=None)    
    verified: bool = Field(default=None)

class VerifyDomainResponse(BaseModel):
    """
    Model representing the response from verifying a domain's DNS configuration in the Naxai email system.
    
    This class provides detailed information about the verification status of all required
    DNS records for a domain, including SPF, DKIM, tracking, MX, and verification token records.
    
    Attributes:
        spf_record (BaseRecord): Verification status of the SPF record.
            Mapped from JSON key 'spfRecord'.
        dkim_record (BaseRecord): Verification status of the DKIM record.
            Mapped from JSON key 'dkimRecord'.
        tracking_record (BaseRecord): Verification status of the tracking CNAME record.
            Mapped from JSON key 'trackingRecord'.
        mx_record (BaseRecord): Verification status of the MX record.
            Mapped from JSON key 'mxRecord'.
        verification_token (BaseRecord): Verification status of the domain ownership token.
            Mapped from JSON key 'verificationToken'.
    
    Example:
        >>> response = VerifyDomainResponse(
        ...     spfRecord=BaseRecord(
        ...         currentValue="v=spf1 include:spf.naxai.com ~all",
        ...         verified=True
        ...     ),
        ...     dkimRecord=BaseRecord(
        ...         currentValue="v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA...",
        ...         verified=True
        ...     ),
        ...     trackingRecord=BaseRecord(
        ...         currentValue="track.naxai.com",
        ...         verified=True
        ...     ),
        ...     mxRecord=BaseRecord(
        ...         currentValue="mx.naxai.com",
        ...         verified=False
        ...     ),
        ...     verificationToken=BaseRecord(
        ...         currentValue="naxai-verification=abc123",
        ...         verified=True
        ...     )
        ... )
        >>> 
        >>> # Check overall verification status
        >>> all_verified = all([
        ...     response.spf_record.verified,
        ...     response.dkim_record.verified,
        ...     response.tracking_record.verified,
        ...     response.mx_record.verified,
        ...     response.verification_token.verified
        ... ])
        >>> print(f"Domain fully verified: {all_verified}")
        >>> 
        >>> # Check which records need attention
        >>> if not response.mx_record.verified:
        ...     print("MX record needs to be configured")
        Domain fully verified: False
        MX record needs to be configured
    
    Note:
        - Each record attribute contains both the current value and verification status
        - A domain is fully verified only when all required records are verified
        - Records with verified=False need to be configured or corrected in the domain's DNS settings
        - Some records may be optional depending on the domain's configuration
        - The verification process checks that the current values match the expected values
    
    See Also:
        BaseRecord: For the structure of individual record verification status
        ExtendedDomainResponse: For the complete domain configuration information
    """
    spf_record: BaseRecord = Field(alias="spfRecord", default=None)
    dkim_record: BaseRecord = Field(alias="dkimRecord", default=None)
    tracking_record: BaseRecord = Field(alias="trackingRecord", default=None)
    mx_record: BaseRecord = Field(alias="mxRecord", default=None)
    verification_token: BaseRecord = Field(alias="verificationToken", default=None)

