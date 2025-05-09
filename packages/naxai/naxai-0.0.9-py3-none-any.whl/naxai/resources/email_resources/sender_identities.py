import json
from typing import Optional
from naxai.models.email.responses.senders_responses import (UpdateSenderResponse,
                                                            GetSenderResponse,
                                                            ListSendersResponse,
                                                            CreateSenderResponse)

class SenderIdentitiesResource:
    """ sender_identities resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/senders"
        self.headers = {"Content-Type": "application/json"}

    #TODO: email validation
    def update(self, sender_id: str, name: str, email: str):
        """
        Update an existing sender identity in the Naxai email system.
        
        This method modifies a sender identity's name and email address. Sender identities
        are used as the "From" address when sending emails through the Naxai platform.
        Updating a sender identity allows you to change its display name or email address
        while maintaining the same sender ID.
        
        Parameters:
            sender_id (str): The unique identifier of the sender identity to update.
                This ID is typically obtained from the create method response or the list method.
            name (str): The new display name for the sender identity.
                This is the name that will appear in the "From" field of emails.
            email (str): The new email address for the sender identity.
                Must be an address from a verified domain in your Naxai account.
        
        Returns:
            UpdateSenderResponse: A response object containing the updated sender identity details:
                - id: Unique identifier for the sender identity
                - name: The updated display name
                - email: The updated email address
                - domain_id: ID of the domain associated with this sender
                - verified: Whether this sender identity is verified
                - shared_with_subaccounts: Whether this sender is shared with subaccounts
                - modified_at: Timestamp when this update was performed
                - modified_by: ID of the user who performed this update
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to update the sender identity
            ValidationError: If the provided email is invalid or not from a verified domain
            ResourceNotFoundError: If the specified sender_id doesn't exist
        
        Example:
            >>> # Update a sender identity's name and email
            >>> updated_sender = client.email.sender_identities.update(
            ...     sender_id="snd_123abc",
            ...     name="Marketing Team",  # Updated name
            ...     email="marketing@example.com"  # Updated email
            ... )
            >>> 
            >>> print(f"Sender updated: {updated_sender.name} <{updated_sender.email}>")
            >>> print(f"Domain ID: {updated_sender.domain_id}")
            >>> print(f"Verification status: {'Verified' if updated_sender.verified else 'Not verified'}")
            >>> print(f"Last modified: {updated_sender.modified_at} by {updated_sender.modified_by}")
            Sender updated: Marketing Team <marketing@example.com>
            Domain ID: dom_456def
            Verification status: Verified
            Last modified: 1703066400000 by usr_789ghi
            
            >>> # Update just the display name, keeping the same email
            >>> current_sender = client.email.sender_identities.get("snd_456def")
            >>> updated = client.email.sender_identities.update(
            ...     sender_id="snd_456def",
            ...     name="Customer Support Team",  # New display name
            ...     email=current_sender.email  # Keep the same email address
            ... )
            >>> 
            >>> print(f"Updated sender name: {updated.name}")
            >>> print(f"Email unchanged: {updated.email}")
            Updated sender name: Customer Support Team
            Email unchanged: support@example.com
        
        Note:
            - The email address must belong to a domain that has been verified in your Naxai account
            - If the email domain changes, the sender identity may require re-verification
            - Updating a sender identity does not affect emails that have already been sent
            - For emails scheduled but not yet sent, the updated sender details will be used
            - The display name can be changed freely without affecting verification status
            - The sender_id remains the same after the update
            - If the update fails due to an invalid email format or domain, an error will be raised
            - This method requires appropriate permissions to modify sender identities
        
        See Also:
            create: For adding a new sender identity
            list: For retrieving multiple sender identities
            get: For retrieving a specific sender identity
            delete: For removing a sender identity
        
        TODO:
            - Add email validation to ensure the provided email is properly formatted
        """
        payload = {
            "name": name,
            "email": email
        }

        return UpdateSenderResponse.model_validate_json(json.dumps(self._client._request("PUT", self.root_path + "/" + sender_id, json=payload, headers=self.headers)))

    def delete(self, sender_id: str):
        """
        Delete a sender identity from the Naxai email system.
        
        This method permanently removes a sender identity identified by its unique ID. Once deleted,
        the sender identity cannot be recovered. This operation is typically used for removing
        sender identities that are no longer needed or were created in error.
        
        Parameters:
            sender_id (str): The unique identifier of the sender identity to delete.
                This ID is typically obtained from the create method response or the list method.
        
        Returns:
            None
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues or invalid sender_id
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to delete the sender identity
            ValidationError: If the sender_id is invalid
            ResourceNotFoundError: If the specified sender_id doesn't exist
            OperationNotAllowedError: If the sender identity cannot be deleted (e.g., if it's in use)
        
        Example:
            >>> # Delete a sender identity that is no longer needed
            >>> try:
            ...     result = client.email.sender_identities.delete("snd_123abc")
            ...     print("Sender identity deleted successfully")
            ... except Exception as e:
            ...     print(f"Failed to delete sender identity: {str(e)}")
            Sender identity deleted successfully
            
            >>> # Attempt to delete a sender identity that is in use
            >>> try:
            ...     client.email.sender_identities.delete("snd_456def")
            ... except Exception as e:
            ...     print(f"Error: {str(e)}")
            Error: Operation not allowed: Cannot delete a sender identity that is in use by active campaigns
        
        Note:
            - This operation permanently removes the sender identity and cannot be undone
            - Sender identities that are currently in use by active or scheduled emails cannot be deleted
            - After deletion, any attempt to access the sender identity using its ID will result in an error
            - If you need to temporarily disable a sender identity, consider updating it instead
            - Deleting a sender identity does not affect the verification status of its associated domain
            - This method is useful for cleaning up unused or outdated sender identities
            - Consider the impact on any templates or automated emails that might reference this sender
        
        See Also:
            create: For adding a new sender identity
            list: For retrieving multiple sender identities
            get: For retrieving a specific sender identity
            update: For modifying an existing sender identity
        """
        return self._client._request("DELETE", self.root_path + "/" + sender_id, headers=self.headers)

    def get(self, sender_id: str):
        """
        Retrieve detailed information about a specific sender identity in the Naxai email system.
        
        This method fetches comprehensive information about a sender identity identified by its unique ID,
        including its name, email address, associated domain, verification status, and sharing settings.
        
        Parameters:
            sender_id (str): The unique identifier of the sender identity to retrieve.
                This ID is typically obtained from the create method response or the list method.
        
        Returns:
            GetSenderResponse: A response object containing detailed sender identity information:
                - id: Unique identifier for the sender identity
                - name: The display name for the sender
                - email: The email address for the sender
                - domain_id: ID of the domain associated with this sender
                - verified: Whether this sender identity is verified
                - shared_with_subaccounts: Whether this sender is shared with subaccounts
                - created_at: Timestamp when the sender identity was created
                - modified_at: Timestamp when the sender identity was last modified
                - modified_by: ID of the user who last modified the sender identity
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues or invalid sender_id
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access the sender identity
            ValidationError: If the sender_id is invalid
            ResourceNotFoundError: If the specified sender_id doesn't exist
        
        Example:
            >>> # Retrieve a specific sender identity by ID
            >>> sender = client.email.sender_identities.get("snd_123abc")
            >>> 
            >>> print(f"Sender: {sender.name} <{sender.email}>")
            >>> print(f"Domain ID: {sender.domain_id}")
            >>> print(f"Verification status: {'Verified' if sender.verified else 'Not verified'}")
            >>> print(f"Shared with subaccounts: {sender.shared_with_subaccounts}")
            >>> print(f"Created at: {sender.created_at}")
            >>> print(f"Last modified: {sender.modified_at} by {sender.modified_by}")
            Sender: Marketing Team <marketing@example.com>
            Domain ID: dom_456def
            Verification status: Verified
            Shared with subaccounts: True
            Created at: 1701066400000
            Last modified: 1703066400000 by usr_789ghi
        
        Note:
            - This method retrieves the complete sender identity information
            - The verification status is important for determining if the sender can be used for sending emails
            - Sender identities must be associated with a verified domain to be usable
            - The shared_with_subaccounts field indicates whether subaccounts can use this sender identity
            - Use this method to check the current state of a sender identity before performing updates
            - If the sender identity doesn't exist or you don't have permission to access it, an error will be raised
        
        See Also:
            create: For adding a new sender identity
            list: For retrieving multiple sender identities
            update: For modifying an existing sender identity
            delete: For removing a sender identity
        """
        return GetSenderResponse.model_validate_json(json.dumps(self._client._request("GET", self.root_path + "/" + sender_id, headers=self.headers)))

    #TODO: email validation
    def create(self, domain_id: str, email: str, name: str):
        """
        Create a new sender identity in the Naxai email system.
        
        This method creates a sender identity that can be used as the "From" address when sending
        emails through the Naxai platform. Sender identities consist of a display name and an email
        address associated with a verified domain in your account.
        
        Parameters:
            domain_id (str): The unique identifier of the domain to associate with this sender.
                The domain must be verified in your Naxai account.
            email (str): The email address for the sender identity.
                Must be an address from the specified domain.
            name (str): The display name for the sender identity.
                This is the name that will appear in the "From" field of emails.
        
        Returns:
            CreateSenderResponse: A response object containing the created sender identity details:
                - id: Unique identifier for the new sender identity
                - name: The display name for the sender
                - email: The email address for the sender
                - domain_id: ID of the domain associated with this sender
                - verified: Whether this sender identity is verified
                - shared_with_subaccounts: Whether this sender is shared with subaccounts
                - created_at: Timestamp when the sender identity was created
                - modified_at: Timestamp when the sender identity was created
                - modified_by: ID of the user who created the sender identity
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to create sender identities
            ValidationError: If the provided email is invalid or not from the specified domain
            ResourceNotFoundError: If the specified domain_id doesn't exist
            DomainNotVerifiedError: If the specified domain is not verified in your account
        
        Example:
            >>> # Create a new sender identity
            >>> new_sender = client.email.sender_identities.create(
            ...     domain_id="dom_123abc",
            ...     email="support@example.com",
            ...     name="Customer Support"
            ... )
            >>> 
            >>> print(f"Sender created: {new_sender.name} <{new_sender.email}>")
            >>> print(f"Sender ID: {new_sender.id}")
            >>> print(f"Verification status: {'Verified' if new_sender.verified else 'Not verified'}")
            >>> print(f"Created at: {new_sender.created_at} by {new_sender.modified_by}")
            Sender created: Customer Support <support@example.com>
            Sender ID: snd_456def
            Verification status: Verified
            Created at: 1703066400000 by usr_789ghi
            
            >>> # Create a sender identity for marketing
            >>> marketing_sender = client.email.sender_identities.create(
            ...     domain_id="dom_123abc",
            ...     email="marketing@example.com",
            ...     name="Marketing Team"
            ... )
            >>> 
            >>> print(f"Marketing sender created with ID: {marketing_sender.id}")
            >>> print(f"From: {marketing_sender.name} <{marketing_sender.email}>")
            Marketing sender created with ID: snd_789ghi
            From: Marketing Team <marketing@example.com>
        
        Note:
            - The domain_id must reference a domain that has been verified in your Naxai account
            - The email address must belong to the specified domain
            - Sender identities are typically verified automatically if the domain is verified
            - New sender identities can be used immediately for sending emails if verified
            - If verification is required, follow the verification process before using the sender
            - The display name can be any string that identifies the sender to recipients
            - Multiple sender identities can be created for the same domain with different email addresses
            - Sender identities are used when sending transactional emails, newsletters, and other communications
            - The created sender identity will have a unique ID that can be used for future operations
        
        See Also:
            list: For retrieving multiple sender identities
            get: For retrieving a specific sender identity
            update: For modifying an existing sender identity
            delete: For removing a sender identity
        
        TODO:
            - Add email validation to ensure the provided email is properly formatted
        """
        payload = {
            "domainId": domain_id,
            "email": email,
            "name": name
        }

        return CreateSenderResponse.model_validate_json(json.dumps(self._client._request("POST", self.root_path, json=payload, headers=self.headers)))

    def list(self,
            domain_id: Optional[str] = None,
            verified: Optional[bool] = None,
            shared: Optional[bool] = None):
        """
        Retrieve a list of sender identities from the Naxai email system.
        
        This method fetches sender identities with optional filtering capabilities, allowing you
        to narrow down results based on domain, verification status, and sharing settings. Sender
        identities are used as the "From" address when sending emails through the Naxai platform.
        
        Parameters:
            domain_id (str, optional): Filter results to sender identities associated with a specific domain.
                If provided, only senders from this domain will be returned.
            verified (bool, optional): Filter results based on verification status.
                If True, only verified sender identities will be returned.
                If False, only unverified sender identities will be returned.
                If None (default), both verified and unverified senders will be returned.
            shared (bool, optional): Filter results based on sharing status with subaccounts.
                If True, only sender identities shared with subaccounts will be returned.
                If False, only sender identities not shared with subaccounts will be returned.
                If None (default), both shared and non-shared senders will be returned.
        
        Returns:
            ListSendersResponse: A response object containing a list of sender identities:
                - Each sender identity in the list includes:
                    - id: Unique identifier for the sender identity
                    - name: The display name for the sender
                    - email: The email address for the sender
                    - domain_id: ID of the domain associated with this sender
                    - verified: Whether this sender identity is verified
                    - shared_with_subaccounts: Whether this sender is shared with subaccounts
                    - created_at: Timestamp when the sender identity was created
                    - modified_at: Timestamp when the sender identity was last modified
                    - modified_by: ID of the user who last modified the sender identity
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to list sender identities
            ValidationError: If any of the provided filter parameters are invalid
        
        Example:
            >>> # Retrieve all sender identities
            >>> all_senders = client.email.sender_identities.list()
            >>> print(f"Found {len(all_senders)} sender identities")
            >>> 
            >>> # Display all senders
            >>> for sender in all_senders:
            ...     verification = "✓" if sender.verified else "✗"
            ...     print(f"{verification} {sender.name} <{sender.email}> (ID: {sender.id})")
            Found 5 sender identities
            ✓ Marketing Team <marketing@example.com> (ID: snd_123abc)
            ✓ Customer Support <support@example.com> (ID: snd_456def)
            ✓ Notifications <noreply@example.com> (ID: snd_789ghi)
            ✗ Sales Team <sales@newdomain.com> (ID: snd_012jkl)
            ✓ Billing <billing@example.com> (ID: snd_345mno)
            
            >>> # Filter by domain
            >>> domain_senders = client.email.sender_identities.list(domain_id="dom_123abc")
            >>> print(f"Found {len(domain_senders)} senders for domain dom_123abc")
            Found 4 senders for domain dom_123abc
            
            >>> # Filter by verification status
            >>> verified_senders = client.email.sender_identities.list(verified=True)
            >>> print(f"Found {len(verified_senders)} verified senders")
            Found 4 verified senders
            
            >>> # Filter by sharing status
            >>> shared_senders = client.email.sender_identities.list(shared=True)
            >>> print(f"Found {len(shared_senders)} senders shared with subaccounts")
            Found 2 senders shared with subaccounts
            
            >>> # Combine filters
            >>> filtered = client.email.sender_identities.list(
            ...     domain_id="dom_123abc",
            ...     verified=True,
            ...     shared=True
            ... )
            >>> print(f"Found {len(filtered)} verified senders from domain dom_123abc shared with subaccounts")
            Found 1 verified senders from domain dom_123abc shared with subaccounts
        
        Note:
            - Without any filters, this method returns all sender identities in your account
            - The domain_id filter is useful when you have multiple domains and want to focus on one
            - The verified filter helps identify sender identities that are ready to use (verified=True)
            or that need attention (verified=False)
            - The shared filter is helpful for managing which sender identities are available to subaccounts
            - Sender identities must be verified before they can be used to send emails
            - Verification typically happens automatically if the sender's domain is verified
            - Results are typically sorted by creation date, with newest senders first
            - This method is useful for:
            * Taking inventory of available sender identities
            * Finding specific senders for use in email campaigns
            * Identifying unverified senders that need attention
            * Managing which senders are shared with subaccounts
        
        See Also:
            create: For adding a new sender identity
            get: For retrieving a specific sender identity by ID
            update: For modifying an existing sender identity
            delete: For removing a sender identity
        """
        params = {}

        if domain_id:
             params["domainId"] = domain_id
        if verified:
             params["verified"] = verified
        if shared:
             params["shared"] = shared

        return ListSendersResponse.model_validate_json(json.dumps(self._client._request("GET", self.root_path, params=params, headers=self.headers)))
