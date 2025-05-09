from pydantic import BaseModel, Field

class BaseSenderResponse(BaseModel):
    """
    Base model representing a sender identity in the Naxai email system.
    
    This class defines the core structure for sender identity data, providing essential
    identification, domain association, and verification status information. It serves
    as the foundation for more specialized sender response models.
    
    Attributes:
        id (str): Unique identifier for the sender identity.
        domain_id (str): Unique identifier of the domain associated with this sender.
            Mapped from JSON key 'domainId'.
        domain_name (str): The fully qualified domain name associated with this sender.
            Mapped from JSON key 'domainName'.
        name (str): The display name for the sender (e.g., "Company Support").
            May be None if not specified.
        email (str): The email address for the sender (e.g., "support@example.com").
            May be None if not specified.
        verified (bool): Whether the sender identity has been verified.
            May be None if verification status is unknown.
        modified_by (str): Identifier of the user who last modified the sender.
            Mapped from JSON key 'modifiedBy'. May be None if not available.
        modified_at (int): Timestamp when the sender was last modified, in milliseconds since epoch.
            Mapped from JSON key 'modifiedAt'. May be None if not available.
    
    Example:
        >>> sender = BaseSenderResponse(
        ...     id="snd_123abc",
        ...     domainId="dom_456def",
        ...     domainName="example.com",
        ...     name="Company Support",
        ...     email="support@example.com",
        ...     verified=True,
        ...     modifiedBy="usr_789ghi",
        ...     modifiedAt=1703066400000
        ... )
        >>> print(f"Sender: {sender.name} <{sender.email}>")
        >>> print(f"Domain: {sender.domain_name} (ID: {sender.domain_id})")
        >>> print(f"Verification status: {'Verified' if sender.verified else 'Not verified'}")
        >>> print(f"Last modified: {sender.modified_at} by {sender.modified_by}")
        Sender: Company Support <support@example.com>
        Domain: example.com (ID: dom_456def)
        Verification status: Verified
        Last modified: 1703066400000 by usr_789ghi
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - It serves as a base class for more specialized sender response models
        - The email address is typically in the format "localpart@domain_name"
        - Sender verification is separate from domain verification
        - A sender must be verified before it can be used to send emails
        - The modified_at timestamp is in milliseconds since epoch
        - Some fields may be None depending on the context and state of the sender
    
    See Also:
        BaseDomainResponse: For the domain information structure
    """
    id: str
    domain_id: str = Field(alias="domainId")
    domain_name: str = Field(alias="domainName")
    name: str = Field(default=None)
    email: str = Field(default=None)
    verified: bool = Field(default=None)
    modified_by: str = Field(alias="modifiedBy", default=None)
    modified_at: int = Field(alias="modifiedAt", default=None)

    model_config = {"populate_by_name": True}

class ListSendersResponse(BaseModel):
    """
    Model representing a list of sender identities in the Naxai email system.
    
    This class behaves like a list of BaseSenderResponse objects while maintaining
    Pydantic validation capabilities. It can parse JSON responses that contain either
    a direct array of senders or an object with a root field containing senders.
    
    Attributes:
        root (list[BaseSenderResponse]): List of sender identity objects.
    
    Example:
        >>> # Creating from a list of senders
        >>> senders_list = ListSendersResponse(
        ...     root=[
        ...         BaseSenderResponse(
        ...             id="snd_123abc",
        ...             domainId="dom_456def",
        ...             domainName="example.com",
        ...             name="Support Team",
        ...             email="support@example.com",
        ...             verified=True
        ...         ),
        ...         BaseSenderResponse(
        ...             id="snd_789ghi",
        ...             domainId="dom_456def",
        ...             domainName="example.com",
        ...             name="Marketing",
        ...             email="marketing@example.com",
        ...             verified=False
        ...         )
        ...     ]
        ... )
        >>> print(f"Found {len(senders_list)} senders")
        >>> for sender in senders_list:
        ...     print(f"Sender: {sender.name} <{sender.email}> - {'Verified' if sender.verified else 'Not verified'}")
        >>> 
        >>> # Parsing from JSON with a direct array
        >>> json_array = '[{"id": "snd_123", "domainId": "dom_456", "domainName": "example.com", "name": "Support", "email": "support@example.com", "verified": true}]'
        >>> parsed = ListSendersResponse.model_validate_json(json_array)
        >>> 
        >>> # Parsing from JSON with a root element
        >>> json_data = '{"root": [{"id": "snd_123", "domainId": "dom_456", "domainName": "example.com", "name": "Support", "email": "support@example.com", "verified": true}]}'
        >>> parsed = ListSendersResponse.model_validate_json(json_data)
        >>> 
        >>> # Finding verified senders
        >>> verified_senders = [sender for sender in senders_list if sender.verified]
        >>> print(f"Found {len(verified_senders)} verified senders")
        Found 2 senders
        Sender: Support Team <support@example.com> - Verified
        Sender: Marketing <marketing@example.com> - Not verified
        Found 1 verified senders
    
    Note:
        - This class behaves like a list, supporting iteration, indexing, and len()
        - It can parse both direct JSON arrays and JSON objects with a 'root' field
        - All senders in the list are BaseSenderResponse objects with complete sender information
        - Senders may be from different domains or the same domain
        - The list may include both verified and unverified senders
        - Only verified senders can be used to send emails
    
    See Also:
        BaseSenderResponse: For the structure of individual sender objects
        CreateSenderResponse: For responses when creating new senders
        GetSenderResponse: For retrieving details of a specific sender
    """
    root: list[BaseSenderResponse] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return the number of senders in the list."""
        return len(self.root)
    
    def __getitem__(self, index):
        """Access senders by index."""
        return self.root[index]
    
    def __iter__(self):
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
    
class CreateSenderResponse(BaseSenderResponse):
    """
    Model representing the response from creating a new sender identity in the Naxai email system.
    
    This class extends BaseSenderResponse to represent the API response when a new sender
    identity is successfully created. It includes all the details of the newly created
    sender, including its verification status and next steps required for verification.
    
    Inherits all attributes from BaseSenderResponse:
        - id (str): Unique identifier for the newly created sender identity
        - domain_id (str): Unique identifier of the domain associated with this sender
        - domain_name (str): The fully qualified domain name associated with this sender
        - name (str): The display name for the sender (e.g., "Company Support")
        - email (str): The email address for the sender (e.g., "support@example.com")
        - verified (bool): Whether the sender identity has been verified (typically false for new senders)
        - modified_by (str): Identifier of the user who created the sender
        - modified_at (int): Timestamp when the sender was created, in milliseconds since epoch
    
    Example:
        >>> response = CreateSenderResponse(
        ...     id="snd_123abc",
        ...     domainId="dom_456def",
        ...     domainName="example.com",
        ...     name="Newsletter",
        ...     email="newsletter@example.com",
        ...     verified=False,
        ...     modifiedBy="usr_789ghi",
        ...     modifiedAt=1703066400000
        ... )
        >>> print(f"Sender created: {response.name} <{response.email}>")
        >>> print(f"Sender ID: {response.id}")
        >>> if not response.verified:
        ...     print("Verification required before sending emails")
        ...     print("Check your inbox for a verification email")
        Sender created: Newsletter <newsletter@example.com>
        Sender ID: snd_123abc
        Verification required before sending emails
        Check your inbox for a verification email
    
    Note:
        - Newly created senders typically have verified=False
        - A verification email is sent to the specified email address
        - The sender must be verified by clicking the link in the verification email
          before it can be used to send emails
        - The domain associated with the sender must also be verified
        - The modified_at timestamp represents the creation time in milliseconds since epoch
        - The modified_by field identifies the user who created the sender
    
    See Also:
        BaseSenderResponse: For the base structure of sender identity information
        GetSenderResponse: For retrieving details of an existing sender
        ListSendersResponse: For retrieving multiple senders
    """

class GetSenderResponse(BaseSenderResponse):
    """
    Model representing the response from retrieving a specific sender identity in the Naxai email system.
    
    This class extends BaseSenderResponse to represent the API response when fetching
    detailed information about an existing sender identity. It includes comprehensive
    information about the sender's configuration, domain association, and verification status.
    
    Inherits all attributes from BaseSenderResponse:
        - id (str): Unique identifier for the sender identity
        - domain_id (str): Unique identifier of the domain associated with this sender
        - domain_name (str): The fully qualified domain name associated with this sender
        - name (str): The display name for the sender (e.g., "Company Support")
        - email (str): The email address for the sender (e.g., "support@example.com")
        - verified (bool): Whether the sender identity has been verified
        - modified_by (str): Identifier of the user who last modified the sender
        - modified_at (int): Timestamp when the sender was last modified, in milliseconds since epoch
    
    Example:
        >>> response = GetSenderResponse(
        ...     id="snd_123abc",
        ...     domainId="dom_456def",
        ...     domainName="example.com",
        ...     name="Support Team",
        ...     email="support@example.com",
        ...     verified=True,
        ...     modifiedBy="usr_789ghi",
        ...     modifiedAt=1703066400000
        ... )
        >>> print(f"Sender: {response.name} <{response.email}>")
        >>> print(f"Domain: {response.domain_name}")
        >>> print(f"Verification status: {'Verified' if response.verified else 'Not verified'}")
        >>> if not response.verified:
        ...     print("This sender cannot be used until verified")
        ...     print("Check the email inbox for a verification link")
        >>> else:
        ...     print("This sender is ready to use for sending emails")
        Sender: Support Team <support@example.com>
        Domain: example.com
        Verification status: Verified
        This sender is ready to use for sending emails
    
    Note:
        - This response provides the current state of a sender identity
        - The verification status (verified) indicates whether the sender can be used to send emails
        - If verified=False, the sender needs to be verified before it can be used
        - Verification typically involves clicking a link sent to the email address
        - The domain associated with the sender must also be verified for the sender to work
        - The modified_at timestamp indicates when the sender was last updated
        - The modified_by field identifies the user who last modified the sender
    
    See Also:
        BaseSenderResponse: For the base structure of sender identity information
        CreateSenderResponse: For responses when creating new senders
        UpdateSenderResponse: For responses when updating existing senders
        ListSendersResponse: For retrieving multiple senders
    """

class UpdateSenderResponse(BaseSenderResponse):
    """
    Model representing the response from updating a sender identity in the Naxai email system.
    
    This class extends BaseSenderResponse to represent the API response when modifying
    an existing sender identity's configuration. It includes the updated sender information
    reflecting the changes that were applied.
    
    Inherits all attributes from BaseSenderResponse:
        - id (str): Unique identifier for the sender identity
        - domain_id (str): Unique identifier of the domain associated with this sender
        - domain_name (str): The fully qualified domain name associated with this sender
        - name (str): The updated display name for the sender (e.g., "Customer Support")
        - email (str): The email address for the sender (e.g., "support@example.com")
        - verified (bool): Whether the sender identity has been verified
        - modified_by (str): Identifier of the user who performed this update
        - modified_at (int): Timestamp when the sender was updated, in milliseconds since epoch
    
    Example:
        >>> response = UpdateSenderResponse(
        ...     id="snd_123abc",
        ...     domainId="dom_456def",
        ...     domainName="example.com",
        ...     name="Customer Support",  # Updated value
        ...     email="support@example.com",
        ...     verified=True,
        ...     modifiedBy="usr_789ghi",  # Updated with current user
        ...     modifiedAt=1703066400000  # Updated with current timestamp
        ... )
        >>> print(f"Sender updated: {response.name} <{response.email}>")
        >>> print(f"Last modified: {response.modified_at} by {response.modified_by}")
        >>> print(f"Verification status: {'Verified' if response.verified else 'Not verified'}")
        Sender updated: Customer Support <support@example.com>
        Last modified: 1703066400000 by usr_789ghi
        Verification status: Verified
    
    Note:
        - The response reflects the sender's state after the update operation
        - The modified_at field will contain the timestamp of this update operation
        - The modified_by field will identify the user who performed this update
        - If the email address was changed, the sender's verification status may be reset to False,
          requiring re-verification before the sender can be used
        - Updates to the display name (name) do not affect verification status
        - The domain associated with the sender cannot be changed; a new sender must be created instead
    
    See Also:
        BaseSenderResponse: For the base structure of sender identity information
        GetSenderResponse: For retrieving the current state of a sender
        CreateSenderResponse: For responses when creating new senders
        ListSendersResponse: For retrieving multiple senders
    """
