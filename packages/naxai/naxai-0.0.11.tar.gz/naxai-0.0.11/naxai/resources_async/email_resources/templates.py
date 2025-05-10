import json
from typing import Optional
from pydantic import Field, validate_call
from naxai.models.email.requests.templates_requests import CreateEmailTemplateRequest
from naxai.models.email.responses.templates_responses import (GetSharedTemplateResponse,
                                                              ListSharedTemplatesRespone,
                                                              UpdateTemplateResponse,
                                                              GetTemplateResponse,
                                                              CreateTemplateResponse,
                                                              ListTemplatesResponse)

class TemplatesResource:
    " templates resource for email resource "
    def __init__(self, client, root_path):
        self._client = client
        self.previous_root = root_path
        self.root_path = root_path + "/templates"
        self.headers = {"Content-Type": "application/json"}

    async def get_shared(self, template_id: str):
        """
        Retrieve a shared email template from the Naxai email system.
        
        This method fetches a specific shared template identified by its unique ID.
        Shared templates are templates that have been made available across multiple
        accounts or teams within the Naxai platform.
        
        Parameters:
            template_id (str): The unique identifier of the shared template to retrieve.
        
        Returns:
            GetSharedTemplateResponse: A response object containing the shared template details:
                - id: Unique identifier for the template
                - name: The name or title of the template
                - source: The content format ("html" or "editor")
                - body: HTML content (if source="html")
                - body_design: Visual editor content (if source="editor")
                - thumbnail: URL or base64 data of a thumbnail image
                - tags: List of tags associated with the template
                - created_at: Timestamp when the template was created
                - created_by: ID of the user who created the template
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues or invalid template_id
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access the shared template
            ValidationError: If the template_id is invalid
            ResourceNotFoundError: If the specified template_id doesn't exist
        
        Example:
            >>> # Retrieve a specific shared template by ID
            >>> shared_template = await client.email.templates.get_shared("tmpl_123abc")
            >>> 
            >>> print(f"Template: {shared_template.name} (ID: {shared_template.id})")
            >>> print(f"Content type: {shared_template.source}")
            >>> print(f"Tags: {', '.join(shared_template.tags)}")
            >>> 
            >>> # Check if it's an HTML template
            >>> if shared_template.source == "html" and shared_template.body:
            ...     print(f"HTML content length: {len(shared_template.body)} characters")
            >>> 
            >>> # Check if it has a thumbnail
            >>> if shared_template.thumbnail:
            ...     print(f"Thumbnail available: {shared_template.thumbnail}")
            Template: Welcome Email (ID: tmpl_123abc)
            Content type: html
            Tags: welcome, onboarding
            HTML content length: 2450 characters
            Thumbnail available: https://example.com/thumbnails/welcome-template.png
        
        Note:
            - Shared templates are read-only and cannot be modified through this API
            - These templates can be used as a starting point for creating your own templates
            - The template content is available in either the body field (for HTML templates)
            or the body_design field (for visual editor templates)
            - Shared templates may include variable placeholders that need to be replaced
            when using the template to send emails
            - The tags field can be used to understand the template's purpose and categorization
        
        See Also:
            list_shared: For retrieving multiple shared templates
        """
        return GetSharedTemplateResponse.model_validate_json(json.dumps(await self._client._request("GET", self.previous_root + "/shared-templates/" + template_id, headers=self.headers)))

    @validate_call
    async def list_shared(self,
                          page: int = Field(default=1),
                          page_size: int = Field(default=25, ge=1, le=100),
                          tags: Optional[list[str]] = Field(default=None, max_length=5)):
        """
        Retrieve a paginated list of shared email templates from the Naxai email system.
        
        This method fetches shared templates with pagination support and optional tag filtering.
        Shared templates are templates that have been made available across multiple accounts
        or teams within the Naxai platform.
        
        Parameters:
            page (int, optional): The page number to retrieve, starting from 1.
                Defaults to 1 (first page).
            page_size (int, optional): Number of templates to return per page.
                Minimum: 1, Maximum: 100, Default: 25.
            tags (list[str], optional): Filter templates by tags. Only templates with at least
                one matching tag will be returned. Maximum 5 tags can be specified.
                Defaults to None (no tag filtering).
        
        Returns:
            ListSharedTemplatesRespone: A response object containing:
                - pagination: Information about the current page and total results
                - items: List of shared template objects, each containing:
                    - id: Unique identifier for the template
                    - name: The name or title of the template
                    - source: The content format ("html" or "editor")
                    - thumbnail: URL or base64 data of a thumbnail image
                    - tags: List of tags associated with the template
                    - created_at: Timestamp when the template was created
                    - created_by: ID of the user who created the template
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to list shared templates
            ValidationError: If the provided parameters are invalid
        
        Example:
            >>> # Retrieve the first page of shared templates (25 per page)
            >>> shared_templates = await client.email.templates.list_shared()
            >>> 
            >>> print(f"Found {shared_templates.pagination.total_items} shared templates")
            >>> print(f"Showing page {shared_templates.pagination.page} of {shared_templates.pagination.total_pages}")
            >>> 
            >>> # Display available templates
            >>> for template in shared_templates.items:
            ...     tags_str = ", ".join(template.tags) if template.tags else "No tags"
            ...     print(f"- {template.name} (ID: {template.id}) - Tags: {tags_str}")
            Found 42 shared templates
            Showing page 1 of 2
            - Welcome Email (ID: tmpl_123abc) - Tags: welcome, onboarding
            - Password Reset (ID: tmpl_456def) - Tags: account, security
            - Order Confirmation (ID: tmpl_789ghi) - Tags: ecommerce, orders
            
            >>> # Filter templates by tags
            >>> onboarding_templates = await client.email.templates.list_shared(tags=["onboarding"])
            >>> print(f"Found {len(onboarding_templates.items)} onboarding templates")
            >>> for template in onboarding_templates.items:
            ...     print(f"- {template.name}")
            Found 3 onboarding templates
            - Welcome Email
            - Getting Started Guide
            - Account Setup
        
        Note:
            - Without any tag filters, this method returns all shared templates available to your account
            - The tag filtering is inclusive - templates matching ANY of the specified tags will be returned
            - Shared templates are read-only and cannot be modified through this API
            - These templates can be used as a starting point for creating your own templates
            - For large collections, use the page parameter to navigate through results
            - The page_size parameter allows customizing how many items to retrieve per request
            - The response includes only basic template information - to get the full template content,
            use the get_shared method with a specific template ID
        
        See Also:
            get_shared: For retrieving a specific shared template by ID
        """
        params = {
            "page": page,
            "pagesize": page_size,
            "tags": tags
        }

        return ListSharedTemplatesRespone.model_validate_json(json.dumps(await self._client._request("GET", self.previous_root + "/shared-templates", params=params, headers=self.headers)))

    async def delete(self, template_id: str):
        """
        Delete an email template from the Naxai email system.
        
        This method permanently removes a template identified by its unique ID. Once deleted,
        the template cannot be recovered. This operation is typically used for removing
        outdated or unused templates.
        
        Parameters:
            template_id (str): The unique identifier of the template to delete.
        
        Returns:
            None
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues or invalid template_id
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to delete the template
            ValidationError: If the template_id is invalid
            ResourceNotFoundError: If the specified template_id doesn't exist
            OperationNotAllowedError: If the template cannot be deleted (e.g., if it's in use)
        
        Example:
            >>> # Delete an outdated template
            >>> try:
            ...     result = await client.email.templates.delete("tmpl_123abc")
            ...     print("Template deleted successfully")
            ... except Exception as e:
            ...     print(f"Failed to delete template: {str(e)}")
            Template deleted successfully
            
            >>> # Attempt to delete a template that is in use
            >>> try:
            ...     await client.email.templates.delete("tmpl_456def")
            ... except Exception as e:
            ...     print(f"Error: {str(e)}")
            Error: Operation not allowed: Cannot delete a template that is in use by active campaigns
        
        Note:
            - This operation permanently removes the template and cannot be undone
            - Templates that are currently in use by active or scheduled emails cannot be deleted
            - After deletion, any attempt to access the template using its ID will result in an error
            - This method is useful for cleaning up unused or outdated templates
            - Consider the impact on any automated emails or newsletters that might reference this template
            - Shared templates cannot be deleted through this method
        
        See Also:
            create: For adding a new template
            list: For retrieving multiple templates
            get: For retrieving a specific template by ID
            update: For modifying an existing template
        """
        return await self._client._request("DELETE", self.root_path + "/" + template_id, headers=self.headers)

    async def update(self, template_id: str, data: CreateEmailTemplateRequest):
        """
        Update an existing email template in the Naxai email system.
        
        This method modifies a template's name, content, or other properties based on the
        provided data. It allows you to keep your templates up-to-date without creating
        new ones for minor changes.
        
        Parameters:
            template_id (str): The unique identifier of the template to update.
            data (CreateEmailTemplateRequest): The updated template configuration containing:
                - name (str, optional): The name or title of the template
                - source (str, optional): Content format, either "html" or "editor"
                - body (str, optional): HTML content (for source="html")
                - body_design (dict, optional): Visual editor content (for source="editor")
                - thumbnail (str, optional): URL or base64 data of a thumbnail image
        
        Returns:
            UpdateTemplateResponse: A response object containing the updated template details:
                - id: Unique identifier for the template
                - name: The updated name or title of the template
                - source: The content format ("html" or "editor")
                - body: HTML content (if source="html")
                - body_design: Visual editor content (if source="editor")
                - thumbnail: URL or base64 data of a thumbnail image
                - modified_at: Timestamp when this update was performed
                - modified_by: ID of the user who performed this update
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to update the template
            ValidationError: If the provided data fails validation
            ResourceNotFoundError: If the specified template_id doesn't exist
        
        Example:
            >>> # Update a template's name and content
            >>> update_data = CreateEmailTemplateRequest(
            ...     name="Updated Welcome Email",
            ...     source="html",
            ...     body="<html><body><h1>Welcome to Our Service!</h1><p>We've updated our welcome message...</p></body></html>"
            ... )
            >>> 
            >>> updated_template = await client.email.templates.update("tmpl_123abc", update_data)
            >>> 
            >>> print(f"Template updated: {updated_template.name}")
            >>> print(f"Content type: {updated_template.source}")
            >>> print(f"Last modified: {updated_template.modified_at} by {updated_template.modified_by}")
            Template updated: Updated Welcome Email
            Content type: html
            Last modified: 1703066400000 by usr_789ghi
            
            >>> # Update just the thumbnail, keeping other properties the same
            >>> thumbnail_update = CreateEmailTemplateRequest(
            ...     thumbnail="https://example.com/thumbnails/new-welcome-image.png"
            ... )
            >>> 
            >>> result = await client.email.templates.update("tmpl_123abc", thumbnail_update)
            >>> print(f"Template thumbnail updated for: {result.name}")
            Template thumbnail updated for: Updated Welcome Email
        
        Note:
            - Only include fields that need to be updated in the request; omitted fields will remain unchanged
            - When updating content, ensure you use the correct source type:
            * For source="html", provide the updated HTML in the body field
            * For source="editor", provide the updated design in the body_design field
            - Changing the source type (from "html" to "editor" or vice versa) requires providing
            the appropriate content field (body or body_design)
            - The modified_at and modified_by fields will be updated to reflect this change
            - Updates to templates do not affect emails that have already been sent
            - For emails scheduled but not yet sent, the updated template will be used
            - Shared templates cannot be updated through this method
        
        See Also:
            create: For adding a new template
            list: For retrieving multiple templates
            get: For retrieving a specific template by ID
            delete: For removing a template
        """
        return UpdateTemplateResponse.model_validate_json(json.dumps(await self._client._request("PUT", self.root_path + "/" + template_id, data=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)))

    async def get(self, template_id: str):
        """
        Retrieve detailed information about a specific email template in the Naxai email system.
        
        This method fetches comprehensive information about a template identified by its unique ID,
        including its name, content, and metadata.
        
        Parameters:
            template_id (str): The unique identifier of the template to retrieve.
        
        Returns:
            GetTemplateResponse: A response object containing detailed template information:
                - id: Unique identifier for the template
                - name: The name or title of the template
                - source: The content format ("html" or "editor")
                - body: HTML content (if source="html")
                - body_design: Visual editor content (if source="editor")
                - thumbnail: URL or base64 data of a thumbnail image
                - created_at: Timestamp when the template was created
                - modified_at: Timestamp when the template was last modified
                - modified_by: ID of the user who last modified the template
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues or invalid template_id
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to access the template
            ValidationError: If the template_id is invalid
            ResourceNotFoundError: If the specified template_id doesn't exist
        
        Example:
            >>> # Retrieve a specific template by ID
            >>> template = await client.email.templates.get("tmpl_123abc")
            >>> 
            >>> print(f"Template: {template.name} (ID: {template.id})")
            >>> print(f"Content type: {template.source}")
            >>> 
            >>> # Display content information based on source type
            >>> if template.source == "html":
            ...     print(f"HTML content length: {len(template.body)} characters")
            ...     print(f"First 100 characters: {template.body[:100]}...")
            ... elif template.source == "editor":
            ...     print(f"Editor blocks: {len(template.body_design.get('blocks', []))}")
            >>> 
            >>> # Check if it has a thumbnail
            >>> if template.thumbnail:
            ...     print(f"Thumbnail available: {template.thumbnail}")
            >>> 
            >>> print(f"Created: {template.created_at}")
            >>> print(f"Last modified: {template.modified_at} by {template.modified_by}")
            Template: Welcome Email (ID: tmpl_123abc)
            Content type: html
            HTML content length: 2450 characters
            First 100 characters: <html><body><h1>Welcome to Our Service!</h1><p>Dear {{user_name}},</p><p>Thank you for joining our...
            Thumbnail available: https://example.com/thumbnails/welcome-template.png
            Created: 1701066400000
            Last modified: 1703066400000 by usr_789ghi
        
        Note:
            - This method retrieves the complete template information, including content
            - For templates with source="html", the body field contains the HTML content
            - For templates with source="editor", the body_design field contains the structured design data
            - Templates may include variable placeholders (e.g., {{user_name}}) that will be
            replaced with actual values when the template is used to send an email
            - Use this method to check the current state of a template before performing updates
            - If the template doesn't exist or you don't have permission to access it, an error will be raised
        
        See Also:
            create: For adding a new template
            list: For retrieving multiple templates
            update: For modifying an existing template
            delete: For removing a template
        """
        return GetTemplateResponse.model_validate_json(json.dumps(await self._client._request("GET", self.root_path + "/" + template_id, headers=self.headers)))

    @validate_call
    async def list(self,
                   page: int = Field(default=1),
                   page_size: int = Field(default=25, ge=1, le=100)
                  ):
        """
        Retrieve a paginated list of email templates from the Naxai email system.
        
        This method fetches templates with pagination support, allowing you to navigate
        through large collections of templates. Results include basic information about
        each template, but not the full content.
        
        Parameters:
            page (int, optional): The page number to retrieve, starting from 1.
                Defaults to 1 (first page).
            page_size (int, optional): Number of templates to return per page.
                Minimum: 1, Maximum: 100, Default: 25.
        
        Returns:
            ListTemplatesResponse: A response object containing:
                - pagination: Information about the current page and total results
                - items: List of template objects, each containing:
                    - id: Unique identifier for the template
                    - name: The name or title of the template
                    - source: The content format ("html" or "editor")
                    - thumbnail: URL or base64 data of a thumbnail image
                    - created_at: Timestamp when the template was created
                    - modified_at: Timestamp when the template was last modified
                    - modified_by: ID of the user who last modified the template
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to list templates
            ValidationError: If the provided parameters are invalid
        
        Example:
            >>> # Retrieve the first page of templates (25 per page)
            >>> templates = await client.email.templates.list()
            >>> 
            >>> print(f"Found {templates.pagination.total_items} templates")
            >>> print(f"Showing page {templates.pagination.page} of {templates.pagination.total_pages}")
            >>> 
            >>> # Display available templates
            >>> for template in templates.items:
            ...     print(f"- {template.name} (ID: {template.id}, Type: {template.source})")
            Found 42 templates
            Showing page 1 of 2
            - Welcome Email (ID: tmpl_123abc, Type: html)
            - Password Reset (ID: tmpl_456def, Type: html)
            - Newsletter Template (ID: tmpl_789ghi, Type: editor)
            
            >>> # Retrieve the second page with 10 items per page
            >>> more_templates = await client.email.templates.list(page=2, page_size=10)
            >>> print(f"Showing {len(more_templates.items)} more templates")
            Showing 10 more templates
        
        Note:
            - Results are typically sorted by creation date, with newest templates first
            - The response includes only basic template information - to get the full template content,
            use the get method with a specific template ID
            - For large collections, use the page parameter to navigate through results
            - The page_size parameter allows customizing how many items to retrieve per request
            - This method returns only your own templates, not shared templates
            - To access shared templates, use the list_shared method
        
        See Also:
            create: For adding a new template
            get: For retrieving a specific template by ID
            update: For modifying an existing template
            delete: For removing a template
            list_shared: For retrieving shared templates
        """
        params = {
            "page": page,
            "pagesize": page_size
        }

        return ListTemplatesResponse.model_validate_json(json.dumps(await self._client._request("GET", self.root_path, params=params, headers=self.headers)))

    async def create(self, data: CreateEmailTemplateRequest):
        """
        Create a new email template in the Naxai email system.
        
        This method creates a template that can be used for sending transactional emails
        or newsletters. Templates provide a reusable structure for emails, allowing for
        consistent branding and efficient email creation.
        
        Parameters:
            data (CreateEmailTemplateRequest): The template configuration containing:
                - name (str): The name or title of the template for internal reference
                - source (str, optional): Content format, either "html" or "editor"
                - body (str, optional): HTML content (required when source="html")
                - body_design (dict, optional): Visual editor content (required when source="editor")
                - thumbnail (str, optional): URL or base64 data of a thumbnail image
        
        Returns:
            CreateTemplateResponse: A response object containing the created template details:
                - id: Unique identifier for the new template
                - name: The name or title of the template
                - source: The content format ("html" or "editor")
                - body: HTML content (if source="html")
                - body_design: Visual editor content (if source="editor")
                - thumbnail: URL or base64 data of a thumbnail image
                - created_at: Timestamp when the template was created
                - modified_at: Timestamp when the template was created
                - modified_by: ID of the user who created the template
        
        Raises:
            NaxaiAPIRequestError: If the API request fails due to invalid parameters or server issues
            NaxaiAuthenticationError: If authentication fails
            NaxaiAuthorizationError: If the account lacks permission to create templates
            ValidationError: If the provided data fails validation
        
        Example:
            >>> # Create a template with HTML content
            >>> template_data = CreateEmailTemplateRequest(
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
            >>> 
            >>> new_template = await client.email.templates.create(template_data)
            >>> 
            >>> print(f"Template created: {new_template.name}")
            >>> print(f"Template ID: {new_template.id}")
            >>> print(f"Content type: {new_template.source}")
            >>> print(f"Created at: {new_template.created_at} by {new_template.modified_by}")
            Template created: Welcome Email Template
            Template ID: tmpl_123abc
            Content type: html
            Created at: 1703066400000 by usr_789ghi
            
            >>> # Create a template with the visual editor
            >>> editor_template = CreateEmailTemplateRequest(
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
            >>> 
            >>> result = await client.email.templates.create(editor_template)
            >>> print(f"Editor template created with ID: {result.id}")
            Editor template created with ID: tmpl_456def
        
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
            - The created template will have a unique ID that can be used for future operations
        
        See Also:
            list: For retrieving multiple templates
            get: For retrieving a specific template by ID
            update: For modifying an existing template
            delete: For removing a template
            list_shared: For browsing shared templates that can be used as starting points
        """
        return CreateTemplateResponse.model_validate_json(json.dumps(await self._client._request("POST", self.root_path, data=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)))