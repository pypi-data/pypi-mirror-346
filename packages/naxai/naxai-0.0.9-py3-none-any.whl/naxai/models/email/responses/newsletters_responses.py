from typing import Literal
from pydantic import BaseModel, Field
from naxai.models.base.pagination import Pagination

#TODO: define body_design
class BaseNewsletterResponse(BaseModel):
    """
    Base model representing a newsletter in the Naxai email system.
    
    This class defines the core structure for newsletter data, providing comprehensive
    information about a newsletter's configuration, content, scheduling, and status.
    It serves as the foundation for more specialized newsletter response models.
    
    Attributes:
        newsletter_id (str): Unique identifier for the newsletter.
            Mapped from JSON key 'newsletterId'.
        name (str): The name or title of the newsletter for internal reference.
        sent_at (int): Timestamp when the newsletter was sent, in milliseconds since epoch.
            Mapped from JSON key 'sentAt'. None if not yet sent.
        scheduled_at (int): Timestamp when the newsletter is scheduled to be sent.
            Mapped from JSON key 'scheduledAt'. None if not scheduled.
        source (Literal["html", "editor"]): The source format of the newsletter content.
            - "html": Raw HTML content provided directly
            - "editor": Content created using the visual editor
        state (Literal["draft", "scheduled", "sent"]): Current state of the newsletter.
            - "draft": Newsletter is in draft mode and not yet scheduled or sent
            - "scheduled": Newsletter is scheduled to be sent at a future time
            - "sent": Newsletter has been sent to recipients
        segment_id (str): Unique identifier of the recipient segment for this newsletter.
            Mapped from JSON key 'segmentId'. None if no segment is specified.
        sender_id (str): Unique identifier of the sender identity used for this newsletter.
            Mapped from JSON key 'senderId'. None if no sender is specified.
        reply_to (str): Email address where replies to this newsletter should be directed.
            Mapped from JSON key 'replyTo'. None if not specified.
        subject (str): The subject line of the newsletter email.
        preheader (str): Preview text that appears after the subject line in email clients.
            None if not specified.
        body (str): The HTML content of the newsletter.
            None if using the visual editor (source="editor").
        body_design (object): The structured design data for newsletters created with the visual editor.
            Mapped from JSON key 'bodyDesign'. None if using raw HTML (source="html").
        thumbnail (str): URL or base64 data of a thumbnail image for the newsletter.
            None if not available.
        preview (str): URL to preview the newsletter in a browser.
            None if not available.
        created_at (int): Timestamp when the newsletter was created, in milliseconds since epoch.
            Mapped from JSON key 'createdAt'. None if not available.
        modified_by (str): Identifier of the user who last modified the newsletter.
            Mapped from JSON key 'modifiedBy'. None if not available.
    
    Example:
        >>> newsletter = BaseNewsletterResponse(
        ...     newsletterId="nws_123abc",
        ...     name="Monthly Update - January 2023",
        ...     sentAt=None,
        ...     scheduledAt=1703066400000,  # January 20, 2023
        ...     source="editor",
        ...     state="scheduled",
        ...     segmentId="seg_456def",
        ...     senderId="snd_789ghi",
        ...     replyTo="support@example.com",
        ...     subject="Your January Newsletter Is Here!",
        ...     preheader="Check out our latest updates and offers",
        ...     body=None,
        ...     bodyDesign={"blocks": [...]},  # Visual editor content structure
        ...     thumbnail="https://example.com/thumbnails/jan-2023.png",
        ...     preview="https://example.com/preview/nws_123abc",
        ...     createdAt=1701066400000,
        ...     modifiedBy="usr_abc123"
        ... )
        >>> print(f"Newsletter: {newsletter.name}")
        >>> print(f"Status: {newsletter.state}")
        >>> if newsletter.state == "scheduled":
        ...     print(f"Scheduled for: {newsletter.scheduled_at}")
        >>> print(f"Subject: {newsletter.subject}")
        >>> print(f"Segment ID: {newsletter.segment_id}")
        Newsletter: Monthly Update - January 2023
        Status: scheduled
        Scheduled for: 1703066400000
        Subject: Your January Newsletter Is Here!
        Segment ID: seg_456def
    
    Note:
        - The body and body_design fields are mutually exclusive based on the source field
        - For source="html", the body field contains the raw HTML content
        - For source="editor", the body_design field contains structured design data
        - The state field indicates where the newsletter is in its lifecycle
        - Timestamps (sent_at, scheduled_at, created_at) are in milliseconds since epoch
        - A newsletter must have a valid sender_id and segment_id to be sent
        - The thumbnail and preview fields provide visual references for the newsletter
    
    See Also:
        CreateNewsletterResponse: For responses when creating new newsletters
        GetNewsletterResponse: For retrieving details of a specific newsletter
        ListNewslettersResponse: For retrieving multiple newsletters
    """
    newsletter_id: str = Field(alias="newsletterId")
    name: str
    sent_at: int = Field(alias="sentAt", default=None)
    scheduled_at: int = Field(alias="scheduledAt", default=None)
    source: Literal["html", "editor"] = Field(default=None)
    state: Literal["draft", "scheduled", "sent"] = Field(default=None)
    segment_id: str = Field(alias="segmentId", default=None)
    sender_id: str = Field(alias="senderId", default=None)
    reply_to: str = Field(alias="replyTo", default=None)
    subject: str
    preheader: str = Field(default=None)
    body: str = Field(default=None)
    body_design: object = Field(alias="bodyDesign", default=None)
    thumbnail: str = Field(default=None)
    preview: str = Field(default=None)
    created_at: int = Field(alias="createdAt", default=None)
    modified_by: str = Field(alias="modifiedBy", default=None)
    modified_at: int = Field(alias="modifiedAt", default=None)

class CreateNewsletterResponse(BaseNewsletterResponse):
    """
    Model representing the response from creating a new newsletter in the Naxai email system.
    
    This class extends BaseNewsletterResponse to represent the API response when a new
    newsletter is successfully created. It includes all the details of the newly created
    newsletter, including its unique identifier, initial state, and configuration.
    
    Inherits all attributes from BaseNewsletterResponse:
        - newsletter_id (str): Unique identifier for the newly created newsletter
        - name (str): The name or title of the newsletter for internal reference
        - sent_at (int): Timestamp when the newsletter was sent (None for new newsletters)
        - scheduled_at (int): Timestamp when the newsletter is scheduled to be sent (if scheduled)
        - source (Literal["html", "editor"]): The source format of the newsletter content
        - state (Literal["draft", "scheduled", "sent"]): Current state (typically "draft" for new newsletters)
        - segment_id (str): Unique identifier of the recipient segment
        - sender_id (str): Unique identifier of the sender identity
        - reply_to (str): Email address where replies should be directed
        - subject (str): The subject line of the newsletter email
        - preheader (str): Preview text that appears after the subject line
        - body (str): The HTML content (for source="html")
        - body_design (object): The structured design data (for source="editor")
        - thumbnail (str): URL or base64 data of a thumbnail image
        - preview (str): URL to preview the newsletter in a browser
        - created_at (int): Timestamp when the newsletter was created
        - modified_by (str): Identifier of the user who created the newsletter
    
    Example:
        >>> response = CreateNewsletterResponse(
        ...     newsletterId="nws_123abc",
        ...     name="Product Launch Announcement",
        ...     source="html",
        ...     state="draft",
        ...     segmentId="seg_456def",
        ...     senderId="snd_789ghi",
        ...     subject="Introducing Our New Product Line",
        ...     body="<html><body><h1>Exciting News!</h1>...</body></html>",
        ...     createdAt=1703066400000,
        ...     modifiedBy="usr_abc123"
        ... )
        >>> print(f"Newsletter created with ID: {response.newsletter_id}")
        >>> print(f"Initial state: {response.state}")
        >>> print(f"To schedule this newsletter, update its scheduled_at field")
        >>> print(f"To preview: {response.preview}")
        Newsletter created with ID: nws_123abc
        Initial state: draft
        To schedule this newsletter, update its scheduled_at field
        To preview: None
    
    Note:
        - Newly created newsletters are typically in the "draft" state
        - The newsletter_id is generated by the system and should be stored for future reference
        - To send the newsletter, it must be updated with a scheduled_at timestamp or sent immediately
        - The created_at timestamp represents the creation time in milliseconds since epoch
        - The modified_by field identifies the user who created the newsletter
        - For newsletters with source="html", the body field contains the HTML content
        - For newsletters with source="editor", the body_design field contains the structured design
        - A preview URL may not be immediately available for newly created newsletters
    
    See Also:
        BaseNewsletterResponse: For the base structure of newsletter information
        GetNewsletterResponse: For retrieving details of an existing newsletter
        UpdateNewsletterResponse: For responses when updating newsletters
        ListNewsLettersResponse: For retrieving multiple newsletters
    """

class ListNewsLettersResponse(BaseModel):
    """
    Model representing a paginated list of newsletters in the Naxai email system.
    
    This class defines the structure for the API response when retrieving multiple
    newsletters, including pagination information and a list of newsletter items.
    It provides a convenient way to access and iterate through newsletter collections.
    
    Attributes:
        pagination (Pagination): Pagination information for the response, including:
            - page: Current page number
            - page_size: Number of items per page
            - total_pages: Total number of pages available
            - total_items: Total number of items across all pages
        items (list[BaseNewsletterResponse]): List of newsletter objects containing
            detailed information about each newsletter. Mapped from JSON key 'items'.
    
    Example:
        >>> response = ListNewsLettersResponse(
        ...     pagination=Pagination(
        ...         page=1,
        ...         page_size=25,
        ...         total_pages=4,
        ...         total_items=87
        ...     ),
        ...     items=[
        ...         BaseNewsletterResponse(
        ...             newsletterId="nws_123abc",
        ...             name="January Newsletter",
        ...             state="sent",
        ...             sentAt=1703066400000,
        ...             subject="January Updates",
        ...             segmentId="seg_456def"
        ...         ),
        ...         BaseNewsletterResponse(
        ...             newsletterId="nws_456def",
        ...             name="February Newsletter",
        ...             state="scheduled",
        ...             scheduledAt=1706744800000,
        ...             subject="February Updates",
        ...             segmentId="seg_456def"
        ...         ),
        ...         BaseNewsletterResponse(
        ...             newsletterId="nws_789ghi",
        ...             name="March Newsletter",
        ...             state="draft",
        ...             subject="March Updates",
        ...             segmentId="seg_456def"
        ...         )
        ...     ]
        ... )
        >>> print(f"Showing page {response.pagination.page} of {response.pagination.total_pages}")
        >>> print(f"Displaying {len(response.items)} of {response.pagination.total_items} total newsletters")
        >>> 
        >>> # Group newsletters by state
        >>> by_state = {"draft": [], "scheduled": [], "sent": []}
        >>> for newsletter in response.items:
        ...     by_state[newsletter.state].append(newsletter)
        >>> 
        >>> print(f"Draft newsletters: {len(by_state['draft'])}")
        >>> print(f"Scheduled newsletters: {len(by_state['scheduled'])}")
        >>> print(f"Sent newsletters: {len(by_state['sent'])}")
        >>> 
        >>> # Find the next scheduled newsletter
        >>> scheduled = [n for n in response.items if n.state == "scheduled"]
        >>> if scheduled:
        ...     next_newsletter = min(scheduled, key=lambda n: n.scheduled_at)
        ...     print(f"Next newsletter: {next_newsletter.name} at {next_newsletter.scheduled_at}")
        Showing page 1 of 4
        Displaying 3 of 87 total newsletters
        Draft newsletters: 1
        Scheduled newsletters: 1
        Sent newsletters: 1
        Next newsletter: February Newsletter at 1706744800000
    
    Note:
        - Use pagination parameters when making API requests to navigate through large result sets
        - The items list contains complete newsletter information as defined in BaseNewsletterResponse
        - Newsletters in the list may be in different states (draft, scheduled, sent)
        - The list may be sorted by creation date, scheduled date, or sent date depending on the API
        - Each newsletter in the list contains its unique ID, which can be used for further operations
        - For large collections, request additional pages by incrementing the page parameter
    
    See Also:
        BaseNewsletterResponse: For the structure of individual newsletter objects
        Pagination: For details about the pagination structure
        CreateNewsletterResponse: For responses when creating new newsletters
        GetNewsletterResponse: For retrieving details of a specific newsletter
    """
    pagination: Pagination
    items: list[BaseNewsletterResponse] = Field(alias="items")

class GetNewsletterResponse(BaseNewsletterResponse):
    """
    Model representing the response from retrieving a specific newsletter in the Naxai email system.
    
    This class extends BaseNewsletterResponse to represent the API response when fetching
    detailed information about an existing newsletter. It includes comprehensive information
    about the newsletter's configuration, content, scheduling, and current status.
    
    Inherits all attributes from BaseNewsletterResponse:
        - newsletter_id (str): Unique identifier for the newsletter
        - name (str): The name or title of the newsletter for internal reference
        - sent_at (int): Timestamp when the newsletter was sent, if applicable
        - scheduled_at (int): Timestamp when the newsletter is scheduled to be sent, if applicable
        - source (Literal["html", "editor"]): The source format of the newsletter content
        - state (Literal["draft", "scheduled", "sent"]): Current state of the newsletter
        - segment_id (str): Unique identifier of the recipient segment
        - sender_id (str): Unique identifier of the sender identity
        - reply_to (str): Email address where replies should be directed
        - subject (str): The subject line of the newsletter email
        - preheader (str): Preview text that appears after the subject line
        - body (str): The HTML content (for source="html")
        - body_design (object): The structured design data (for source="editor")
        - thumbnail (str): URL or base64 data of a thumbnail image
        - preview (str): URL to preview the newsletter in a browser
        - created_at (int): Timestamp when the newsletter was created
        - modified_by (str): Identifier of the user who last modified the newsletter
        - modified_at (int): Timestamp when the newsletter was last modified
    
    Example:
        >>> response = GetNewsletterResponse(
        ...     newsletterId="nws_123abc",
        ...     name="Monthly Update - January 2023",
        ...     sentAt=1703066400000,
        ...     source="editor",
        ...     state="sent",
        ...     segmentId="seg_456def",
        ...     senderId="snd_789ghi",
        ...     replyTo="support@example.com",
        ...     subject="Your January Newsletter Is Here!",
        ...     preheader="Check out our latest updates and offers",
        ...     bodyDesign={"blocks": [...]},
        ...     thumbnail="https://example.com/thumbnails/jan-2023.png",
        ...     preview="https://example.com/preview/nws_123abc",
        ...     createdAt=1701066400000,
        ...     modifiedAt=1702066400000,
        ...     modifiedBy="usr_abc123"
        ... )
        >>> print(f"Newsletter: {response.name} (ID: {response.newsletter_id})")
        >>> print(f"Current state: {response.state}")
        >>> 
        >>> # Display different information based on state
        >>> if response.state == "draft":
        ...     print("This newsletter is still in draft mode and hasn't been scheduled")
        ... elif response.state == "scheduled":
        ...     print(f"Scheduled to send at: {response.scheduled_at}")
        ... elif response.state == "sent":
        ...     print(f"Sent at: {response.sent_at}")
        >>> 
        >>> print(f"Preview URL: {response.preview}")
        >>> print(f"Created: {response.created_at}")
        >>> print(f"Last modified: {response.modified_at} by {response.modified_by}")
        Newsletter: Monthly Update - January 2023 (ID: nws_123abc)
        Current state: sent
        Sent at: 1703066400000
        Preview URL: https://example.com/preview/nws_123abc
        Created: 1701066400000
        Last modified: 1702066400000 by usr_abc123
    
    Note:
        - This response provides the current state of a newsletter, including its content and configuration
        - The state field indicates where the newsletter is in its lifecycle (draft, scheduled, sent)
        - For newsletters with state="sent", the sent_at field contains the sending timestamp
        - For newsletters with state="scheduled", the scheduled_at field contains the future sending time
        - For newsletters with source="html", the body field contains the complete HTML content
        - For newsletters with source="editor", the body_design field contains the structured design data
        - The preview URL can be used to view the newsletter in a browser
        - The modified_at and modified_by fields track the last update to the newsletter
    
    See Also:
        BaseNewsletterResponse: For the base structure of newsletter information
        CreateNewsletterResponse: For responses when creating new newsletters
        UpdateNewsletterResponse: For responses when updating newsletters
        ListNewsLettersResponse: For retrieving multiple newsletters
    """

class UpdateNewsletterResponse(BaseNewsletterResponse):
    """
    Model representing the response from updating a newsletter in the Naxai email system.
    
    This class extends BaseNewsletterResponse to represent the API response when modifying
    an existing newsletter's configuration or content. It includes the updated newsletter
    information reflecting the changes that were applied.
    
    Inherits all attributes from BaseNewsletterResponse:
        - newsletter_id (str): Unique identifier for the newsletter
        - name (str): The name or title of the newsletter (may be updated)
        - sent_at (int): Timestamp when the newsletter was sent, if applicable
        - scheduled_at (int): Timestamp when the newsletter is scheduled to be sent (may be updated)
        - source (Literal["html", "editor"]): The source format of the newsletter content
        - state (Literal["draft", "scheduled", "sent"]): Current state (may change based on updates)
        - segment_id (str): Unique identifier of the recipient segment (may be updated)
        - sender_id (str): Unique identifier of the sender identity (may be updated)
        - reply_to (str): Email address where replies should be directed (may be updated)
        - subject (str): The subject line of the newsletter email (may be updated)
        - preheader (str): Preview text that appears after the subject line (may be updated)
        - body (str): The HTML content for source="html" (may be updated)
        - body_design (object): The structured design data for source="editor" (may be updated)
        - thumbnail (str): URL or base64 data of a thumbnail image (may be updated)
        - preview (str): URL to preview the newsletter in a browser
        - created_at (int): Timestamp when the newsletter was created
        - modified_by (str): Identifier of the user who performed this update
        - modified_at (int): Timestamp when this update was performed
    
    Example:
        >>> response = UpdateNewsletterResponse(
        ...     newsletterId="nws_123abc",
        ...     name="Monthly Update - January 2023 (Revised)",  # Updated value
        ...     scheduledAt=1703156400000,  # Updated value
        ...     source="editor",
        ...     state="scheduled",  # Changed from "draft" to "scheduled"
        ...     segmentId="seg_456def",
        ...     senderId="snd_789ghi",
        ...     subject="Your January Newsletter Is Here! (Updated)",  # Updated value
        ...     bodyDesign={"blocks": [...]},  # Updated content
        ...     preview="https://example.com/preview/nws_123abc",
        ...     createdAt=1701066400000,
        ...     modifiedAt=1702066400000,  # Updated with current timestamp
        ...     modifiedBy="usr_abc123"  # Updated with current user
        ... )
        >>> print(f"Newsletter updated: {response.name}")
        >>> print(f"Current state: {response.state}")
        >>> if response.state == "scheduled":
        ...     print(f"Scheduled to send at: {response.scheduled_at}")
        >>> print(f"Preview URL: {response.preview}")
        >>> print(f"Last modified: {response.modified_at} by {response.modified_by}")
        Newsletter updated: Monthly Update - January 2023 (Revised)
        Current state: scheduled
        Scheduled to send at: 1703156400000
        Preview URL: https://example.com/preview/nws_123abc
        Last modified: 1702066400000 by usr_abc123
    
    Note:
        - The response reflects the newsletter's state after the update operation
        - The modified_at field will contain the timestamp of this update operation
        - The modified_by field will identify the user who performed this update
        - If the newsletter was previously in "draft" state and scheduled_at was set,
          the state may automatically change to "scheduled"
        - Updates to content (body or body_design) will be reflected in the preview URL
        - Once a newsletter has been sent (state="sent"), most fields cannot be updated
        - The state transition rules are:
          * draft -> scheduled (when scheduled_at is set)
          * draft -> sent (when sent immediately)
          * scheduled -> sent (when send time arrives or sent manually)
          * scheduled -> draft (when unscheduled)
    
    See Also:
        BaseNewsletterResponse: For the base structure of newsletter information
        GetNewsletterResponse: For retrieving the current state of a newsletter
        CreateNewsletterResponse: For responses when creating new newsletters
        ListNewsLettersResponse: For retrieving multiple newsletters
    """