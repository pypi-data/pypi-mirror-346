from typing import Optional, Literal
from pydantic import BaseModel, Field

#TODO: url validation (thumbnail)
#TODO: verify required properties
class CreateEmailTemplateRequest(BaseModel):
    """
    Model representing a request to create an email template in the Naxai email system.
    
    This class defines the structure for email template creation requests, providing
    the necessary fields to specify template content, format, and metadata. Email templates
    serve as reusable content structures for both transactional emails and newsletters,
    allowing for consistent branding and efficient email creation.
    
    Attributes:
        name (str): The name or title of the template for internal reference.
            Maximum 255 characters.
        source (Optional[Literal["html", "editor"]]): The source format of the template content.
            - "html": Raw HTML content provided directly
            - "editor": Content created using the visual editor
            Defaults to None.
        body (Optional[str]): The HTML content of the template.
            Required when source="html". Defaults to None.
        body_design (Optional[dict]): The structured design data for templates created with the visual editor.
            Required when source="editor". Mapped from JSON key 'bodyDesign'. Defaults to None.
        thumbnail (Optional[str]): URL or base64 data of a thumbnail image for the template.
            Defaults to None.
    
    Example:
        >>> # Creating a template with HTML content
        >>> template = CreateEmailTemplateRequest(
        ...     name="Welcome Email Template",
        ...     source="html",
        ...     body=" \
        ...         <html> \
        ...         <body> \
        ...             <h1>Welcome to Our Service!</h1> \
        ...             <p>Dear {{user_name}},</p> \
        ...             <p>Thank you for joining our platform. We're excited to have you on board!</p> \
        ...             <p>Your account has been successfully created and is ready to use.</p> \
        ...             <p>Best regards,<br>The Team</p> \
        ...         </body> \
        ...         </html> \
        ...     ",
        ...     thumbnail="https://example.com/thumbnails/welcome-template.png"
        ... )
        >>> print(f"Template: {template.name}")
        >>> print(f"Source type: {template.source}")
        >>> print(f"Has HTML content: {bool(template.body)}")
        Template: Welcome Email Template
        Source type: html
        Has HTML content: True
        
        >>> # Creating a template with the visual editor
        >>> template = CreateEmailTemplateRequest(
        ...     name="Newsletter Template",
        ...     source="editor",
        ...     body_design={
        ...         "blocks": [
        ...             {"type": "header", "text": "{{newsletter_title}}"},
        ...             {"type": "text", "text": "{{newsletter_intro}}"},
        ...             {"type": "image", "url": "{{feature_image}}"},
        ...             {"type": "button", "text": "Read More", "url": "{{article_url}}"}
        ...         ]
        ...     }
        ... )
        >>> print(f"Template: {template.name}")
        >>> print(f"Created with: {template.source}")
        >>> print(f"Has design data: {bool(template.body_design)}")
        Template: Newsletter Template
        Created with: editor
        Has design data: True
    
    Note:
        - The name field should be descriptive to help identify the template's purpose
        - The source field determines which content field is required:
          * For source="html", the body field must contain the HTML content
          * For source="editor", the body_design field must contain the structured design data
        - Templates can include variable placeholders (e.g., {{user_name}}) that will be
          replaced with actual values when the template is used to send an email
        - HTML templates should be well-formed and ideally responsive for proper display
          across different email clients and devices
        - The thumbnail provides a visual reference for the template in the template library
        - Templates can be used for both transactional emails and newsletters
    
    TODO:
        - Add URL validation for the thumbnail field
        - Verify required properties based on the source field (body or body_design)
    """

    name: str = Field(max_length=255)
    source: Optional[Literal["html", "editor"]] = Field(default=None)
    body: Optional[str] = Field(default=None)
    body_design: Optional[dict] = Field(default=None, alias="bodyDesign")
    thumbnail: Optional[str] = Field(default=None)

    