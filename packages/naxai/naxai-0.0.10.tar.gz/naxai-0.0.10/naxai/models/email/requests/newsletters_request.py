from typing import Optional, Literal
from pydantic import BaseModel, Field

#TODO: url validations ( thumbnail, preview )
#TODO: verify required props ( segment_id, source, sender_id, reply_to, etc ...)
#TODO: email validation ( reply_to )

class CreateEmailNewsletterRequest(BaseModel):
    """
    Model representing a request to create a newsletter in the Naxai email system.
    
    This class defines the structure for newsletter creation requests, providing all the
    necessary fields to specify newsletter content, scheduling, recipients, and delivery options.
    Newsletters are typically used for marketing communications, updates, and regular
    communications with subscribers.
    
    Attributes:
        name (str): The name or title of the newsletter for internal reference.
            Maximum 255 characters.
        scheduled_at (Optional[int]): Timestamp when the newsletter should be sent,
            in milliseconds since epoch. If not provided, the newsletter will be saved as a draft.
            Mapped from JSON key 'scheduledAt'. Defaults to None.
        source (Optional[Literal["html", "editor"]]): The source format of the newsletter content.
            - "html": Raw HTML content provided directly
            - "editor": Content created using the visual editor
            Defaults to None.
        segment_id (Optional[str]): Unique identifier of the recipient segment for this newsletter.
            Mapped from JSON key 'segmentId'. Defaults to None.
        sender_id (Optional[str]): Unique identifier of the sender identity used for this newsletter.
            Mapped from JSON key 'senderId'. Defaults to None.
        reply_to (Optional[str]): Email address where replies to this newsletter should be directed.
            Mapped from JSON key 'replyTo'. Defaults to None.
        subject (Optional[str]): The subject line of the newsletter email.
            Maximum 255 characters. Defaults to None.
        pre_header (Optional[str]): Preview text that appears after the subject line in email clients.
            Maximum 255 characters. Mapped from JSON key 'preheader'. Defaults to None.
        body (Optional[str]): The HTML content of the newsletter.
            Required when source="html". Defaults to None.
        body_design (Optional[dict]): The structured design data for newsletters created with the visual editor.
            Required when source="editor". Mapped from JSON key 'bodyDesign'. Defaults to None.
        thumbnail (Optional[str]): URL or base64 data of a thumbnail image for the newsletter.
            Defaults to None.
        preview (Optional[str]): URL to preview the newsletter in a browser.
            Defaults to None.
    
    Example:
        >>> # Creating a draft newsletter with HTML content
        >>> newsletter = CreateEmailNewsletterRequest(
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
        >>> print(f"Newsletter: {newsletter.name}")
        >>> print(f"Subject: {newsletter.subject}")
        >>> print(f"Status: {'Scheduled' if newsletter.scheduled_at else 'Draft'}")
        Newsletter: Monthly Newsletter - January 2023
        Subject: Your January Newsletter Is Here!
        Status: Draft
        
        >>> # Creating a scheduled newsletter with the visual editor
        >>> import time
        >>> next_week = int(time.time() * 1000) + (7 * 24 * 60 * 60 * 1000)  # One week from now
        >>> 
        >>> newsletter = CreateEmailNewsletterRequest(
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
        >>> print(f"Newsletter: {newsletter.name}")
        >>> print(f"Scheduled for: {newsletter.scheduled_at}")
        >>> print(f"Created with: {newsletter.source}")
        Newsletter: Product Launch Announcement
        Scheduled for: 1703671200000
        Created with: editor
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - Required fields depend on the intended use:
          * For draft newsletters: name, source, and either body (for HTML) or body_design (for editor)
          * For scheduled newsletters: All of the above plus scheduled_at, segment_id, sender_id, and subject
        - The body and body_design fields are mutually exclusive based on the source field:
          * For source="html", the body field must contain the HTML content
          * For source="editor", the body_design field must contain the structured design data
        - The segment_id determines which subscribers will receive the newsletter
        - The sender_id must reference a verified sender identity in your Naxai account
        - The pre_header is important for improving open rates as it appears in email previews
        - The scheduled_at timestamp is in milliseconds since epoch
        - If scheduled_at is provided, the newsletter will be automatically sent at that time
        - If scheduled_at is not provided, the newsletter will be saved as a draft for later scheduling
    
    TODO:
        - Add URL validations for thumbnail and preview fields
        - Verify required properties based on context (segment_id, source, sender_id, reply_to, etc.)
        - Add email validation for reply_to field
    """
    name: str = Field(max_length=255)
    scheduled_at: Optional[int] = Field(default=None, alias="scheduledAt")
    source: Optional[Literal["html", "editor"]] = Field(default=None)
    segment_id: Optional[str] = Field(default=None, alias="segmentId")
    sender_id: Optional[str] = Field(default=None, alias="senderId")
    reply_to: Optional[str] = Field(default=None, alias="replyTo")
    subject: Optional[str] = Field(default=None, max_length=255)
    pre_header: Optional[str] = Field(default=None, alias="preheader", max_length=255)
    body: Optional[str] = Field(default=None)
    body_design: Optional[dict] = Field(default=None, alias="bodyDesign")
    thumbnail: Optional[str] = Field(default=None)
    preview: Optional[str] = Field(default=None)

    model_config = {"populate_by_name": True}