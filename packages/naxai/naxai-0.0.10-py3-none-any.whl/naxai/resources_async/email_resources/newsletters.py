import json
from pydantic import Field, validate_call
from naxai.models.email.requests.newsletters_request import CreateEmailNewsletterRequest
from naxai.models.email.responses.newsletters_responses import (CreateNewsletterResponse,
                                                                UpdateNewsletterResponse,
                                                                ListNewsLettersResponse,
                                                                GetNewsletterResponse)

class NewslettersResource:
    """ newsletters resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/newsletters"
        self.headers = {"Content-Type": "application/json"}

    async def create(self, data:CreateEmailNewsletterRequest):
        """
        Create a new newsletter in the Naxai email system.
        
        This method creates a newsletter based on the provided configuration, which can be
        either saved as a draft or scheduled for immediate or future delivery. Newsletters
        can be created with either raw HTML content or structured content from the visual editor.
        
        Parameters:
            data (CreateEmailNewsletterRequest): The newsletter configuration object containing:
                - name (str): The name or title of the newsletter (required)
                - scheduled_at (int, optional): Timestamp when to send the newsletter
                - source (str): Content format, either "html" or "editor" (required)
                - segment_id (str, optional): ID of the recipient segment
                - sender_id (str, optional): ID of the sender identity
                - reply_to (str, optional): Email address for replies
                - subject (str, optional): The subject line of the newsletter
                - pre_header (str, optional): Preview text shown in email clients
                - body (str, optional): HTML content (required when source="html")
                - body_design (dict, optional): Visual editor content (required when source="editor")
                - thumbnail (str, optional): URL or base64 data of a thumbnail image
                - preview (str, optional): URL to preview the newsletter
        
        Returns:
            CreateNewsletterResponse: A response object containing the created newsletter details:
                - newsletter_id: Unique identifier for the new newsletter
                - name: The name or title of the newsletter
                - state: Initial state ("draft" or "scheduled")
                - scheduled_at: Timestamp when the newsletter is scheduled (if applicable)
                - source: The content format ("html" or "editor")
                - segment_id: ID of the recipient segment
                - sender_id: ID of the sender identity
                - subject: The subject line of the newsletter
                - and other newsletter properties
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to create newsletters
            ValidationError: If the provided data fails validation
        
        Example:
            >>> # Create a draft newsletter with HTML content
            >>> newsletter_request = CreateEmailNewsletterRequest(
            ...     name="Monthly Newsletter - January 2023",
            ...     source="html",
            ...     segment_id="seg_123abc",
            ...     sender_id="snd_456def",
            ...     reply_to="newsletter@example.com",
            ...     subject="Your January Newsletter Is Here!",
            ...     pre_header="Check out our latest updates and offers",
            ...     body="<html><body><h1>January Newsletter</h1><p>Welcome to our monthly update...</p></body></html>",
            ...     thumbnail="https://example.com/thumbnails/jan-2023.png"
            ... )
            >>> 
            >>> new_newsletter = await client.email.newsletters.create(newsletter_request)
            >>> 
            >>> print(f"Newsletter created with ID: {new_newsletter.newsletter_id}")
            >>> print(f"Initial state: {new_newsletter.state}")
            >>> print(f"Preview URL: {new_newsletter.preview}")
            Newsletter created with ID: nws_123abc
            Initial state: draft
            Preview URL: https://example.com/preview/nws_123abc
            
            >>> # Create a scheduled newsletter with the visual editor
            >>> import time
            >>> next_week = int(time.time() * 1000) + (7 * 24 * 60 * 60 * 1000)  # One week from now
            >>> 
            >>> scheduled_newsletter = CreateEmailNewsletterRequest(
            ...     name="Product Launch Announcement",
            ...     scheduled_at=next_week,
            ...     source="editor",
            ...     segment_id="seg_customers",
            ...     sender_id="snd_marketing",
            ...     subject="Introducing Our New Product Line",
            ...     pre_header="Exciting new products now available",
            ...     body_design={
            ...         "blocks": [
            ...             {"type": "header", "text": "Introducing Our New Product Line"},
            ...             {"type": "text", "text": "We're excited to announce our latest products..."}
            ...         ]
            ...     }
            ... )
            >>> 
            >>> result = await client.email.newsletters.create(scheduled_newsletter)
            >>> 
            >>> print(f"Scheduled newsletter created: {result.name}")
            >>> print(f"Will be sent at: {result.scheduled_at}")
            >>> print(f"To segment: {result.segment_id}")
            Scheduled newsletter created: Product Launch Announcement
            Will be sent at: 1703671200000
            To segment: seg_customers
        
        Note:
            - Newsletters are created in "draft" state unless a scheduled_at timestamp is provided
            - For newsletters with source="html", the body field must contain valid HTML content
            - For newsletters with source="editor", the body_design field must contain structured design data
            - The segment_id determines which subscribers will receive the newsletter
            - The sender_id must reference a verified sender identity in your Naxai account
            - The reply_to email address will receive replies to the newsletter
            - The pre_header is important for improving open rates as it appears in email previews
            - After creating a draft newsletter, you can later schedule it using the update method
            - The created newsletter will have a unique newsletter_id that can be used for future operations
            - A preview URL is typically generated for the newsletter, allowing you to view it before sending
        
        See Also:
            list: For retrieving multiple newsletters
            get: For retrieving a specific newsletter by ID
            update: For modifying an existing newsletter
            delete: For removing a newsletter
        """
        return CreateNewsletterResponse.model_validate_json(json.dumps(await self._client._request("POST", self.root_path, data=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)))

    @validate_call
    async def list(self, page: int = 1, page_size: int = Field(default=25, le=100, ge=1)):
        """
        Retrieve a paginated list of newsletters from the Naxai email system.
        
        This method fetches newsletters with pagination support, allowing you to navigate
        through large collections of newsletters. Results include comprehensive information
        about each newsletter's configuration, content, scheduling, and current status.
        
        Parameters:
            page (int, optional): The page number to retrieve, starting from 1.
                Defaults to 1 (first page).
            page_size (int, optional): Number of newsletters to return per page.
                Minimum: 1, Maximum: 100, Default: 25.
        
        Returns:
            ListNewsLettersResponse: A response object containing:
                - pagination: Information about the current page and total results
                - items: List of newsletter objects, each containing:
                    - newsletter_id: Unique identifier for the newsletter
                    - name: The name or title of the newsletter
                    - sent_at: Timestamp when the newsletter was sent (if applicable)
                    - scheduled_at: Timestamp when the newsletter is scheduled (if applicable)
                    - source: The content format ("html" or "editor")
                    - state: Current state ("draft", "scheduled", or "sent")
                    - segment_id: ID of the recipient segment
                    - sender_id: ID of the sender identity
                    - subject: The subject line of the newsletter
                    - and other newsletter properties
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to list newsletters
            ValidationError: If the provided parameters are invalid
        
        Example:
            >>> # Retrieve the first page of newsletters (25 per page)
            >>> newsletters = await client.email.newsletters.list()
            >>> 
            >>> print(f"Found {newsletters.pagination.total_items} newsletters")
            >>> print(f"Showing page {newsletters.pagination.page} of {newsletters.pagination.total_pages}")
            >>> 
            >>> # Display newsletters by state
            >>> for newsletter in newsletters.items:
            ...     status = newsletter.state
            ...     if status == "scheduled":
            ...         date_info = f"scheduled for {newsletter.scheduled_at}"
            ...     elif status == "sent":
            ...         date_info = f"sent at {newsletter.sent_at}"
            ...     else:
            ...         date_info = "in draft"
            ...     print(f"- {newsletter.name}: {status} ({date_info})")
            Found 87 newsletters
            Showing page 1 of 4
            - January Newsletter: sent (sent at 1703066400000)
            - February Newsletter: scheduled (scheduled for 1706744800000)
            - March Newsletter: draft (in draft)
            
            >>> # Retrieve the second page with 50 items per page
            >>> more_newsletters = await client.email.newsletters.list(page=2, page_size=50)
            >>> print(f"Showing {len(more_newsletters.items)} more newsletters")
            Showing 37 more newsletters
        
        Note:
            - Results are typically sorted by creation date, with newest newsletters first
            - The response includes newsletters in all states (draft, scheduled, sent)
            - For large collections, use the page parameter to navigate through results
            - The page_size parameter allows customizing how many items to retrieve per request
            - Timestamps (sent_at, scheduled_at) are in milliseconds since epoch
            - Use the newsletter_id from results to perform operations on specific newsletters
        
        See Also:
            create: For adding a new newsletter
            get: For retrieving a specific newsletter by ID
            update: For modifying an existing newsletter
            delete: For removing a newsletter
        """
        params = {
            "page": page,
            "pagesize": page_size
        }
        return ListNewsLettersResponse.model_validate_json(json.dumps(await self._client._request("GET", self.root_path, params=params, headers=self.headers)))

    async def get(self, newsletter_id: str):
        """
        Retrieve detailed information about a specific newsletter in the Naxai email system.
        
        This method fetches comprehensive information about a newsletter identified by its unique ID,
        including its configuration, content, scheduling status, and current state. It provides
        access to all newsletter properties, including content and design data.
        
        Parameters:
            newsletter_id (str): The unique identifier of the newsletter to retrieve.
                This ID is typically obtained from the create method response or the list method.
        
        Returns:
            GetNewsletterResponse: A response object containing detailed newsletter information:
                - newsletter_id: Unique identifier for the newsletter
                - name: The name or title of the newsletter
                - sent_at: Timestamp when the newsletter was sent (if applicable)
                - scheduled_at: Timestamp when the newsletter is scheduled (if applicable)
                - source: The content format ("html" or "editor")
                - state: Current state ("draft", "scheduled", or "sent")
                - segment_id: ID of the recipient segment
                - sender_id: ID of the sender identity
                - reply_to: Email address for replies
                - subject: The subject line of the newsletter
                - preheader: Preview text shown in email clients
                - body: HTML content (if source="html")
                - body_design: Visual editor content (if source="editor")
                - thumbnail: URL or base64 data of a thumbnail image
                - preview: URL to preview the newsletter
                - created_at: Timestamp when the newsletter was created
                - modified_by: ID of the user who last modified the newsletter
                - modified_at: Timestamp when the newsletter was last modified
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues or invalid newsletter_id
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access the newsletter
            ValidationError: If the newsletter_id is invalid
        
        Example:
            >>> # Retrieve a specific newsletter by ID
            >>> newsletter = await client.email.newsletters.get("nws_123abc")
            >>> 
            >>> print(f"Newsletter: {newsletter.name} (ID: {newsletter.newsletter_id})")
            >>> print(f"Current state: {newsletter.state}")
            >>> 
            >>> # Display different information based on state
            >>> if newsletter.state == "draft":
            ...     print("This newsletter is still in draft mode and hasn't been scheduled")
            ... elif newsletter.state == "scheduled":
            ...     print(f"Scheduled to send at: {newsletter.scheduled_at}")
            ... elif newsletter.state == "sent":
            ...     print(f"Sent at: {newsletter.sent_at}")
            >>> 
            >>> # Display recipient and sender information
            >>> print(f"Segment ID: {newsletter.segment_id}")
            >>> print(f"Sender ID: {newsletter.sender_id}")
            >>> print(f"Reply-to: {newsletter.reply_to}")
            >>> 
            >>> # Display content information
            >>> print(f"Subject: {newsletter.subject}")
            >>> print(f"Preheader: {newsletter.preheader}")
            >>> print(f"Content type: {newsletter.source}")
            >>> 
            >>> # Access preview URL
            >>> print(f"Preview URL: {newsletter.preview}")
            Newsletter: Monthly Update - January 2023 (ID: nws_123abc)
            Current state: scheduled
            Scheduled to send at: 1703066400000
            Segment ID: seg_456def
            Sender ID: snd_789ghi
            Reply-to: support@example.com
            Subject: Your January Newsletter Is Here!
            Preheader: Check out our latest updates and offers
            Content type: editor
            Preview URL: https://example.com/preview/nws_123abc
        
        Note:
            - This method retrieves the complete newsletter information, including content
            - For newsletters with source="html", the body field contains the HTML content
            - For newsletters with source="editor", the body_design field contains the structured design data
            - The state field indicates where the newsletter is in its lifecycle (draft, scheduled, sent)
            - For newsletters with state="scheduled", the scheduled_at field contains the future sending time
            - For newsletters with state="sent", the sent_at field contains the sending timestamp
            - The preview URL can be used to view the newsletter in a browser
            - Use this method to check the current state of a newsletter before performing updates
            - If the newsletter doesn't exist or you don't have permission to access it, an error will be raised
        
        See Also:
            create: For adding a new newsletter
            list: For retrieving multiple newsletters
            update: For modifying an existing newsletter
            delete: For removing a newsletter
        """
        return GetNewsletterResponse.model_validate_json(json.dumps(await self._client._request("GET", self.root_path + "/" + newsletter_id, headers=self.headers)))

    async def update(self, data: CreateEmailNewsletterRequest, newsletter_id: str):
        """
        Update an existing newsletter in the Naxai email system.
        
        This method modifies a newsletter's configuration, content, or scheduling based on the
        provided data. It can be used to update draft newsletters, schedule newsletters for
        delivery, or modify scheduled newsletters that haven't been sent yet.
        
        Parameters:
            data (CreateEmailNewsletterRequest): The updated newsletter configuration containing:
                - name (str, optional): The name or title of the newsletter
                - scheduled_at (int, optional): Timestamp when to send the newsletter
                - source (str, optional): Content format, either "html" or "editor"
                - segment_id (str, optional): ID of the recipient segment
                - sender_id (str, optional): ID of the sender identity
                - reply_to (str, optional): Email address for replies
                - subject (str, optional): The subject line of the newsletter
                - pre_header (str, optional): Preview text shown in email clients
                - body (str, optional): HTML content (for source="html")
                - body_design (dict, optional): Visual editor content (for source="editor")
                - thumbnail (str, optional): URL or base64 data of a thumbnail image
                - preview (str, optional): URL to preview the newsletter
            newsletter_id (str): The unique identifier of the newsletter to update.
                This ID is typically obtained from the create method response or the list method.
        
        Returns:
            UpdateNewsletterResponse: A response object containing the updated newsletter details:
                - newsletter_id: Unique identifier for the newsletter
                - name: The name or title of the newsletter
                - state: Current state ("draft", "scheduled", or "sent")
                - scheduled_at: Timestamp when the newsletter is scheduled (if applicable)
                - source: The content format ("html" or "editor")
                - segment_id: ID of the recipient segment
                - sender_id: ID of the sender identity
                - subject: The subject line of the newsletter
                - and other newsletter properties
                - modified_at: Timestamp when this update was performed
                - modified_by: ID of the user who performed this update
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to update the newsletter
            ValidationError: If the provided data fails validation
            ResourceNotFoundError: If the specified newsletter_id doesn't exist
        
        Example:
            >>> # First, retrieve the newsletter to update
            >>> newsletter = await client.email.newsletters.get("nws_123abc")
            >>> print(f"Current state: {newsletter.state}")
            >>> print(f"Current subject: {newsletter.subject}")
            Current state: draft
            Current subject: Draft Newsletter
            >>> 
            >>> # Create an update request with modified fields
            >>> import time
            >>> tomorrow = int(time.time() * 1000) + (24 * 60 * 60 * 1000)  # Tomorrow
            >>> 
            >>> update_request = CreateEmailNewsletterRequest(
            ...     name=newsletter.name,  # Keep the same name
            ...     scheduled_at=tomorrow,  # Schedule it for tomorrow
            ...     subject="Updated Newsletter Subject",  # Change the subject
            ...     segment_id=newsletter.segment_id,  # Keep the same segment
            ...     sender_id=newsletter.sender_id  # Keep the same sender
            ... )
            >>> 
            >>> # Update the newsletter
            >>> updated = await client.email.newsletters.update(update_request, newsletter.newsletter_id)
            >>> 
            >>> print(f"Newsletter updated: {updated.name}")
            >>> print(f"New state: {updated.state}")
            >>> print(f"New subject: {updated.subject}")
            >>> print(f"Scheduled for: {updated.scheduled_at}")
            >>> print(f"Last modified: {updated.modified_at} by {updated.modified_by}")
            Newsletter updated: Monthly Newsletter
            New state: scheduled
            New subject: Updated Newsletter Subject
            Scheduled for: 1703152800000
            Last modified: 1703066400000 by usr_abc123
            
            >>> # Update content of an existing newsletter
            >>> existing = await client.email.newsletters.get("nws_456def")
            >>> 
            >>> # Update only the content, keeping other properties the same
            >>> content_update = CreateEmailNewsletterRequest(
            ...     source="html",
            ...     body="<html><body><h1>Updated Content</h1><p>This is the revised newsletter content.</p></body></html>"
            ... )
            >>> 
            >>> result = await client.email.newsletters.update(content_update, existing.newsletter_id)
            >>> print(f"Content updated for: {result.name}")
            >>> print(f"Preview URL: {result.preview}")
            Content updated for: Product Announcement
            Preview URL: https://example.com/preview/nws_456def
        
        Note:
            - Only include fields that need to be updated in the request; omitted fields will remain unchanged
            - Adding a scheduled_at timestamp to a draft newsletter will change its state to "scheduled"
            - Setting scheduled_at to None for a scheduled newsletter will change its state back to "draft"
            - Once a newsletter has been sent (state="sent"), most fields cannot be updated
            - When updating content, ensure you use the correct source type:
            * For source="html", provide the updated HTML in the body field
            * For source="editor", provide the updated design in the body_design field
            - Changing the source type (from "html" to "editor" or vice versa) requires providing
            the appropriate content field (body or body_design)
            - The state transition rules are:
            * draft -> scheduled (when scheduled_at is set)
            * scheduled -> draft (when scheduled_at is removed)
            * draft/scheduled -> sent (when the newsletter is sent, either manually or automatically)
            - The modified_at and modified_by fields will be updated to reflect this change
            - The preview URL can be used to view the updated newsletter in a browser
        
        See Also:
            create: For adding a new newsletter
            list: For retrieving multiple newsletters
            get: For retrieving a specific newsletter by ID
            delete: For removing a newsletter
        """
        return UpdateNewsletterResponse.model_validate_json(json.dumps(await self._client._request("PUT", self.root_path + "/" + newsletter_id, data=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)))

    async def delete(self, newsletter_id: str):
        """
        Delete a newsletter from the Naxai email system.
        
        This method permanently removes a newsletter identified by its unique ID. Once deleted,
        the newsletter cannot be recovered. This operation is typically used for removing draft
        or outdated newsletters that are no longer needed.
        
        Parameters:
            newsletter_id (str): The unique identifier of the newsletter to delete.
                This ID is typically obtained from the create method response or the list method.
        
        Returns:
            dict: A response object indicating the success of the deletion operation.
                Typically contains a success indicator and/or a confirmation message.
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues or invalid newsletter_id
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to delete the newsletter
            ValidationError: If the newsletter_id is invalid
            ResourceNotFoundError: If the specified newsletter_id doesn't exist
            OperationNotAllowedError: If the newsletter cannot be deleted (e.g., if it has been sent)
        
        Example:
            >>> # First, retrieve a list of draft newsletters
            >>> newsletters = await client.email.newsletters.list()
            >>> drafts = [n for n in newsletters.items if n.state == "draft"]
            >>> 
            >>> if drafts:
            ...     # Select an outdated draft to delete
            ...     old_draft = drafts[0]
            ...     print(f"Deleting draft newsletter: {old_draft.name} (ID: {old_draft.newsletter_id})")
            ...     
            ...     # Delete the newsletter
            ...     result = await client.email.newsletters.delete(old_draft.newsletter_id)
            ...     print("Newsletter deleted successfully")
            ...     
            ...     # Verify deletion by trying to retrieve it
            ...     try:
            ...         await client.email.newsletters.get(old_draft.newsletter_id)
            ...     except Exception as e:
            ...         print(f"Verification confirmed: {str(e)}")
            ... else:
            ...     print("No draft newsletters available to delete")
            Deleting draft newsletter: Outdated Announcement (ID: nws_123abc)
            Newsletter deleted successfully
            Verification confirmed: Resource not found: Newsletter with ID nws_123abc does not exist
            
            >>> # Attempt to delete a newsletter that has already been sent
            >>> try:
            ...     await client.email.newsletters.delete("nws_456def")  # ID of a sent newsletter
            ... except Exception as e:
            ...     print(f"Error: {str(e)}")
            Error: Operation not allowed: Cannot delete a newsletter that has already been sent
        
        Note:
            - This operation permanently removes the newsletter and cannot be undone
            - It's recommended to verify the newsletter state before deletion
            - Typically, only newsletters in "draft" state can be deleted
            - Newsletters in "scheduled" state may need to be unscheduled first (by updating with scheduled_at=None)
            - Newsletters in "sent" state often cannot be deleted due to record-keeping requirements
            - After deletion, any attempt to access the newsletter using its ID will result in an error
            - This method is useful for cleaning up unused or outdated draft newsletters
            - Consider archiving important newsletters instead of deleting them if they may be needed for reference
        
        See Also:
            create: For adding a new newsletter
            list: For retrieving multiple newsletters
            get: For retrieving a specific newsletter by ID
            update: For modifying an existing newsletter or unscheduling a scheduled newsletter
        """
        return await self._client._request("DELETE", self.root_path + "/" + newsletter_id, headers=self.headers)