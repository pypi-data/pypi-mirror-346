from typing import Optional, Literal
from pydantic import BaseModel, Field
from naxai.models.base.pagination import Pagination


class BaseResponse(BaseModel):
    """
    Base model representing an email template in the Naxai email system.
    
    This class defines the core structure for email template data, providing essential
    information about a template's configuration, content, and metadata. It serves as
    the foundation for more specialized template response models.
    
    Attributes:
        template_id (str): Unique identifier for the template.
            Mapped from JSON key 'templateId'.
        name (Optional[str]): The name or title of the template for reference.
            May be None if not specified.
        source (Optional[Literal["html", "editor"]]): The source format of the template content.
            - "html": Raw HTML content provided directly
            - "editor": Content created using the visual editor
            May be None if not specified.
        body (Optional[str]): The HTML content of the template.
            Only populated when source="html". May be None if using the visual editor
            or if not specified.
        body_design (Optional[object]): The structured design data for templates created with the visual editor.
            Only populated when source="editor". Mapped from JSON key 'bodyDesign'.
            May be None if using raw HTML or if not specified.
        thumbnail (Optional[str]): URL or base64 data of a thumbnail image for the template.
            May be None if not available.
        created_at (Optional[int]): Timestamp when the template was created, in milliseconds since epoch.
            Mapped from JSON key 'createdAt'. May be None if not available.
        modified_at (Optional[int]): Timestamp when the template was last modified, in milliseconds since epoch.
            Mapped from JSON key 'modifiedAt'. May be None if not available.
        modified_by (Optional[str]): Identifier of the user who last modified the template.
            Mapped from JSON key 'modifiedBy'. May be None if not available.
    
    Example:
        >>> template = BaseResponse(
        ...     templateId="tpl_123abc",
        ...     name="Welcome Email",
        ...     source="html",
        ...     body="<html><body><h1>Welcome!</h1><p>Thank you for joining us.</p></body></html>",
        ...     thumbnail="https://example.com/thumbnails/welcome.png",
        ...     createdAt=1703066400000,
        ...     modifiedAt=1703066500000,
        ...     modifiedBy="usr_789xyz"
        ... )
        >>> print(f"Template: {template.name} (ID: {template.template_id})")
        >>> print(f"Source type: {template.source}")
        >>> if template.source == "html":
        ...     print(f"HTML content length: {len(template.body)} characters")
        >>> print(f"Last modified: {template.modified_at} by {template.modified_by}")
        Template: Welcome Email (ID: tpl_123abc)
        Source type: html
        HTML content length: 76 characters
        Last modified: 1703066500000 by usr_789xyz
        
        >>> # Template created with the visual editor
        >>> editor_template = BaseResponse(
        ...     templateId="tpl_456def",
        ...     name="Newsletter Template",
        ...     source="editor",
        ...     bodyDesign={"blocks": [{"type": "header", "text": "Monthly Newsletter"}]},
        ...     thumbnail="https://example.com/thumbnails/newsletter.png",
        ...     createdAt=1703066400000
        ... )
        >>> print(f"Template: {editor_template.name}")
        >>> print(f"Created with: {editor_template.source}")
        >>> print(f"Has design data: {editor_template.body_design is not None}")
        Template: Newsletter Template
        Created with: editor
        Has design data: True
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - It serves as a base class for more specialized template response models
        - The body and body_design fields are mutually exclusive based on the source field
        - For source="html", the body field contains the raw HTML content
        - For source="editor", the body_design field contains structured design data
        - Timestamps (created_at, modified_at) are in milliseconds since epoch
        - Most fields are optional as they may not be included in all API responses
    
    See Also:
        CreateTemplateResponse: For responses when creating new templates
        GetTemplateResponse: For retrieving details of a specific template
        UpdateTemplateResponse: For responses when updating templates
        ListTemplatesResponse: For retrieving multiple templates
    """
    template_id: str = Field(alias="templateId")
    name: Optional[str] = Field(default=None)
    source: Optional[Literal["html", "editor"]] = Field(default=None)
    body: Optional[str] = Field(default=None)
    body_design: Optional[object] = Field(default=None, alias="bodyDesign")
    thumbnail: Optional[str] = Field(default=None)
    created_at: Optional[int] = Field(default=None, alias="createdAt")
    modified_at: Optional[int] = Field(default=None, alias="modifiedAt")
    modified_by: Optional[str] = Field(default=None, alias="modifiedBy") 

    model_config = {"populate_by_name": True}

class SharedTemplatesBaseResponse(BaseModel):
    """
    Base model representing a shared email template in the Naxai email system.
    
    This class defines the core structure for shared template data, providing essential
    information about a template that is shared across users or organizations. It serves
    as the foundation for more specialized shared template response models.
    
    Attributes:
        shared_template_id (str): Unique identifier for the shared template.
            Mapped from JSON key 'sharedTemplateId'.
        name (Optional[str]): The name or title of the shared template for reference.
            May be None if not specified.
        thumbnail (Optional[str]): URL or base64 data of a thumbnail image for the template.
            May be None if not available.
        preview (Optional[str]): URL to preview the template in a browser.
            May be None if not available.
        tags (Optional[list[str]]): List of tags associated with the shared template for categorization.
            May be None if no tags are assigned.
    
    Example:
        >>> template = SharedTemplatesBaseResponse(
        ...     sharedTemplateId="stpl_123abc",
        ...     name="Marketing Newsletter",
        ...     thumbnail="https://example.com/thumbnails/marketing.png",
        ...     preview="https://example.com/preview/stpl_123abc",
        ...     tags=["marketing", "newsletter", "promotional"]
        ... )
        >>> print(f"Shared Template: {template.name} (ID: {template.shared_template_id})")
        >>> print(f"Preview URL: {template.preview}")
        >>> print(f"Tags: {', '.join(template.tags)}")
        Shared Template: Marketing Newsletter (ID: stpl_123abc)
        Preview URL: https://example.com/preview/stpl_123abc
        Tags: marketing, newsletter, promotional
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - It serves as a base class for more specialized shared template response models
        - Shared templates are typically pre-designed templates available to all users
        - The content (body or body_design) is not included in this base response
        - To access the content, use the GetSharedTemplateResponse class
    
    See Also:
        GetSharedTemplateResponse: For retrieving complete details of a shared template
        ListSharedTemplatesRespone: For retrieving multiple shared templates
    """
    shared_template_id: str = Field(alias="sharedTemplateId")
    name: Optional[str] = Field(default=None)
    thumbnail: Optional[str] = Field(default=None)
    preview: Optional[str] = Field(default=None)
    tags: Optional[list[str]] = Field(default=None)

    model_config = {"populate_by_name": True}

class CreateTemplateResponse(BaseResponse):
    """
    Model representing the response from creating a new email template in the Naxai email system.
    
    This class extends BaseResponse to represent the API response when a new
    email template is successfully created. It includes all the details of the newly created
    template, including its unique identifier, content, and metadata.
    
    Inherits all attributes from BaseResponse:
        - template_id (str): Unique identifier for the newly created template
        - name (Optional[str]): The name or title of the template
        - source (Optional[Literal["html", "editor"]]): The source format of the template content
        - body (Optional[str]): The HTML content (for source="html")
        - body_design (Optional[object]): The structured design data (for source="editor")
        - thumbnail (Optional[str]): URL or base64 data of a thumbnail image
        - created_at (Optional[int]): Timestamp when the template was created
        - modified_at (Optional[int]): Timestamp when the template was last modified
        - modified_by (Optional[str]): Identifier of the user who created the template
    
    Example:
        >>> response = CreateTemplateResponse(
        ...     templateId="tpl_123abc",
        ...     name="Welcome Email",
        ...     source="html",
        ...     body="<html><body><h1>Welcome!</h1><p>Thank you for joining us.</p></body></html>",
        ...     createdAt=1703066400000,
        ...     modifiedAt=1703066400000,
        ...     modifiedBy="usr_789xyz"
        ... )
        >>> print(f"Template created with ID: {response.template_id}")
        >>> print(f"Template name: {response.name}")
        >>> print(f"Creation time: {response.created_at}")
        Template created with ID: tpl_123abc
        Template name: Welcome Email
        Creation time: 1703066400000
    
    Note:
        - The created_at and modified_at timestamps will typically be the same for newly created templates
        - The template_id is generated by the system and should be stored for future reference
        - For templates with source="html", the body field contains the HTML content
        - For templates with source="editor", the body_design field contains the structured design
    
    See Also:
        BaseResponse: For the base structure of template information
        GetTemplateResponse: For retrieving details of an existing template
        UpdateTemplateResponse: For responses when updating templates
    """
    
class ListTemplatesResponse(BaseModel):
    """
    Model representing a paginated list of email templates in the Naxai email system.
    
    This class defines the structure for the API response when retrieving multiple
    email templates, including pagination information and a list of template items.
    
    Attributes:
        pagination (Pagination): Pagination information for the response, including:
            - page: Current page number
            - page_size: Number of items per page
            - total_pages: Total number of pages available
            - total_items: Total number of templates across all pages
        items (list[BaseResponse]): List of template objects containing
            detailed information about each email template.
    
    Example:
        >>> response = ListTemplatesResponse(
        ...     pagination=Pagination(
        ...         page=1,
        ...         page_size=25,
        ...         total_pages=2,
        ...         total_items=30
        ...     ),
        ...     items=[
        ...         BaseResponse(
        ...             templateId="tpl_123abc",
        ...             name="Welcome Email",
        ...             source="html",
        ...             createdAt=1703066400000
        ...         ),
        ...         BaseResponse(
        ...             templateId="tpl_456def",
        ...             name="Newsletter Template",
        ...             source="editor",
        ...             createdAt=1702980000000
        ...         )
        ...     ]
        ... )
        >>> print(f"Showing page {response.pagination.page} of {response.pagination.total_pages}")
        >>> print(f"Displaying {len(response.items)} of {response.pagination.total_items} total templates")
        >>> 
        >>> # List all templates
        >>> for template in response.items:
        ...     print(f"- {template.name} (ID: {template.template_id}, Type: {template.source})")
        Showing page 1 of 2
        Displaying 2 of 30 total templates
        - Welcome Email (ID: tpl_123abc, Type: html)
        - Newsletter Template (ID: tpl_456def, Type: editor)
    
    Note:
        - Use pagination parameters when making API requests to navigate through large result sets
        - The items list contains template information as defined in BaseResponse
        - Each template in the list contains its unique ID, which can be used for further operations
        - For large collections, request additional pages by incrementing the page parameter
    
    See Also:
        BaseResponse: For the structure of individual template objects
        Pagination: For details about the pagination structure
    """
    pagination: Pagination
    items: list[BaseResponse]

class GetTemplateResponse(BaseResponse):
    """
    Model representing the response from retrieving a specific email template in the Naxai email system.
    
    This class extends BaseResponse to represent the API response when fetching detailed
    information about an existing email template by its ID. It includes comprehensive
    information about the template's configuration, content, and metadata.
    
    Inherits all attributes from BaseResponse:
        - template_id (str): Unique identifier for the template
        - name (Optional[str]): The name or title of the template
        - source (Optional[Literal["html", "editor"]]): The source format of the template content
        - body (Optional[str]): The HTML content (for source="html")
        - body_design (Optional[object]): The structured design data (for source="editor")
        - thumbnail (Optional[str]): URL or base64 data of a thumbnail image
        - created_at (Optional[int]): Timestamp when the template was created
        - modified_at (Optional[int]): Timestamp when the template was last modified
        - modified_by (Optional[str]): Identifier of the user who last modified the template
    
    Example:
        >>> response = GetTemplateResponse(
        ...     templateId="tpl_123abc",
        ...     name="Welcome Email",
        ...     source="html",
        ...     body="<html><body><h1>Welcome!</h1><p>Thank you for joining us.</p></body></html>",
        ...     thumbnail="https://example.com/thumbnails/welcome.png",
        ...     createdAt=1703066400000,
        ...     modifiedAt=1703066500000,
        ...     modifiedBy="usr_789xyz"
        ... )
        >>> print(f"Template: {response.name} (ID: {response.template_id})")
        >>> print(f"Source type: {response.source}")
        >>> if response.source == "html":
        ...     print(f"HTML content: {response.body[:50]}...")
        >>> print(f"Created: {response.created_at}")
        >>> print(f"Last modified: {response.modified_at} by {response.modified_by}")
        Template: Welcome Email (ID: tpl_123abc)
        Source type: html
        HTML content: <html><body><h1>Welcome!</h1><p>Thank you for joini...
        Created: 1703066400000
        Last modified: 1703066500000 by usr_789xyz
    
    Note:
        - This response provides the complete details of a single email template
        - For templates with source="html", the body field contains the complete HTML content
        - For templates with source="editor", the body_design field contains the complete structured design
        - The created_at and modified_at timestamps provide the template's history
        - The modified_by field identifies the user who last modified the template
    
    See Also:
        BaseResponse: For the base structure of template information
        CreateTemplateResponse: For responses when creating new templates
        UpdateTemplateResponse: For responses when updating templates
    """

class UpdateTemplateResponse(BaseResponse):
    """
    Model representing the response from updating an email template in the Naxai email system.
    
    This class extends BaseResponse to represent the API response when modifying
    an existing email template's configuration or content. It includes the updated template
    information reflecting the changes that were applied.
    
    Inherits all attributes from BaseResponse:
        - template_id (str): Unique identifier for the template
        - name (Optional[str]): The name or title of the template (may be updated)
        - source (Optional[Literal["html", "editor"]]): The source format of the template content
        - body (Optional[str]): The HTML content (for source="html", may be updated)
        - body_design (Optional[object]): The structured design data (for source="editor", may be updated)
        - thumbnail (Optional[str]): URL or base64 data of a thumbnail image (may be updated)
        - created_at (Optional[int]): Timestamp when the template was created
        - modified_at (Optional[int]): Timestamp when the template was updated (updated with current time)
        - modified_by (Optional[str]): Identifier of the user who performed this update
    
    Example:
        >>> response = UpdateTemplateResponse(
        ...     templateId="tpl_123abc",
        ...     name="Updated Welcome Email",  # Updated value
        ...     source="html",
        ...     body="<html><body><h1>Welcome!</h1><p>Thank you for joining our platform.</p></body></html>",  # Updated content
        ...     thumbnail="https://example.com/thumbnails/welcome-updated.png",  # Updated thumbnail
        ...     createdAt=1703066400000,
        ...     modifiedAt=1703152800000,  # Updated with current timestamp
        ...     modifiedBy="usr_789xyz"  # Updated with current user
        ... )
        >>> print(f"Template updated: {response.name} (ID: {response.template_id})")
        >>> print(f"Last modified: {response.modified_at} by {response.modified_by}")
        Template updated: Updated Welcome Email (ID: tpl_123abc)
        Last modified: 1703152800000 by usr_789xyz
    
    Note:
        - The response reflects the template's state after the update operation
        - The modified_at field will contain the timestamp of this update operation
        - The modified_by field will identify the user who performed this update
        - The created_at field remains unchanged from the original creation time
        - For templates with source="html", the body field contains the updated HTML content
        - For templates with source="editor", the body_design field contains the updated structured design
    
    See Also:
        BaseResponse: For the base structure of template information
        GetTemplateResponse: For retrieving the current state of a template
        CreateTemplateResponse: For responses when creating new templates
    """

class ListSharedTemplatesRespone(BaseModel):
    """
    Model representing a paginated list of shared email templates in the Naxai email system.
    
    This class defines the structure for the API response when retrieving multiple
    shared email templates, including pagination information and a list of template items.
    
    Attributes:
        pagination (Pagination): Pagination information for the response, including:
            - page: Current page number
            - page_size: Number of items per page
            - total_pages: Total number of pages available
            - total_items: Total number of shared templates across all pages
        items (list[SharedTemplatesBaseResponse]): List of shared template objects containing
            information about each shared email template.
    
    Example:
        >>> response = ListSharedTemplatesRespone(
        ...     pagination=Pagination(
        ...         page=1,
        ...         page_size=25,
        ...         total_pages=3,
        ...         total_items=65
        ...     ),
        ...     items=[
        ...         SharedTemplatesBaseResponse(
        ...             sharedTemplateId="stpl_123abc",
        ...             name="Marketing Newsletter",
        ...             thumbnail="https://example.com/thumbnails/marketing.png",
        ...             tags=["marketing", "newsletter"]
        ...         ),
        ...         SharedTemplatesBaseResponse(
        ...             sharedTemplateId="stpl_456def",
        ...             name="Product Announcement",
        ...             thumbnail="https://example.com/thumbnails/product.png",
        ...             tags=["product", "announcement"]
        ...         )
        ...     ]
        ... )
        >>> print(f"Showing page {response.pagination.page} of {response.pagination.total_pages}")
        >>> print(f"Displaying {len(response.items)} of {response.pagination.total_items} total shared templates")
        >>> 
        >>> # List all shared templates
        >>> for template in response.items:
        ...     tags = ", ".join(template.tags) if template.tags else "No tags"
        ...     print(f"- {template.name} (ID: {template.shared_template_id}, Tags: {tags})")
        Showing page 1 of 3
        Displaying 2 of 65 total shared templates
        - Marketing Newsletter (ID: stpl_123abc, Tags: marketing, newsletter)
        - Product Announcement (ID: stpl_456def, Tags: product, announcement)
    
    Note:
        - Use pagination parameters when making API requests to navigate through large result sets
        - The items list contains shared template information as defined in SharedTemplatesBaseResponse
        - Each shared template in the list contains its unique ID, which can be used to retrieve full details
        - The content (body or body_design) is not included in the list response
        - For large collections, request additional pages by incrementing the page parameter
    
    See Also:
        SharedTemplatesBaseResponse: For the structure of individual shared template objects
        GetSharedTemplateResponse: For retrieving complete details of a specific shared template
        Pagination: For details about the pagination structure
    """
    pagination: Pagination
    items: list[SharedTemplatesBaseResponse]

class GetSharedTemplateResponse(SharedTemplatesBaseResponse):
    """
    Model representing the response from retrieving a specific shared email template in the Naxai email system.
    
    This class extends SharedTemplatesBaseResponse to include the content of the shared template,
    providing comprehensive information about a shared template's configuration, content, and metadata.
    
    Attributes:
        body (Optional[str]): The HTML content of the shared template.
            Only populated when the template uses raw HTML. May be None if using the visual editor
            or if not specified.
        body_design (Optional[object]): The structured design data for templates created with the visual editor.
            Only populated when the template uses the visual editor. Mapped from JSON key 'bodyDesign'.
            May be None if using raw HTML or if not specified.
            
        # Inherited from SharedTemplatesBaseResponse:
        shared_template_id (str): Unique identifier for the shared template.
        name (Optional[str]): The name or title of the shared template.
        thumbnail (Optional[str]): URL or base64 data of a thumbnail image.
        preview (Optional[str]): URL to preview the template in a browser.
        tags (Optional[list[str]]): List of tags associated with the shared template.
    
    Example:
        >>> response = GetSharedTemplateResponse(
        ...     sharedTemplateId="stpl_123abc",
        ...     name="Marketing Newsletter",
        ...     thumbnail="https://example.com/thumbnails/marketing.png",
        ...     preview="https://example.com/preview/stpl_123abc",
        ...     tags=["marketing", "newsletter"],
        ...     body="<html><body><h1>Marketing Newsletter</h1><p>Your content here.</p></body></html>"
        ... )
        >>> print(f"Shared Template: {response.name} (ID: {response.shared_template_id})")
        >>> print(f"Preview URL: {response.preview}")
        >>> print(f"Tags: {', '.join(response.tags) if response.tags else 'No tags'}")
        >>> print(f"Has HTML content: {response.body is not None}")
        >>> print(f"Has design data: {response.body_design is not None}")
        Shared Template: Marketing Newsletter (ID: stpl_123abc)
        Preview URL: https://example.com/preview/stpl_123abc
        Tags: marketing, newsletter
        Has HTML content: True
        Has design data: False
    
    Note:
        - This class supports both alias-based and direct field name access through populate_by_name
        - The body and body_design fields are mutually exclusive
        - For HTML templates, the body field contains the complete HTML content
        - For visual editor templates, the body_design field contains the structured design data
        - Shared templates can be used as a starting point for creating new custom templates
        - The preview URL can be used to view the rendered template in a browser
    
    See Also:
        SharedTemplatesBaseResponse: For the base structure of shared template information
        ListSharedTemplatesRespone: For retrieving multiple shared templates
    """
    body: Optional[str] = Field(default=None)
    body_design: Optional[object] = Field(default=None, alias="bodyDesign")

    model_config = {"populate_by_name": True}

