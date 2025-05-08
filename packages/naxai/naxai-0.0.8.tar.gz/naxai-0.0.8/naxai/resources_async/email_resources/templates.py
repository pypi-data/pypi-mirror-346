from typing import Optional
from pydantic import Field, validate_call
from naxai.models.email.create_email_template import CreateEmailTemplateRequest

class TemplatesResource:
    " templates resource for email resource "
    def __init__(self, client, root_path):
        self._client = client
        self.previous_root = root_path
        self.root_path = root_path + "/templates"
        self.headers = {"Content-Type": "application/json"}
            
    async def get_shared(self, template_id: str):
        """
        Get a shared email template.

        Args:
            template_id (str): The ID of the shared template to retrieve.

        Returns:
            dict: The API response containing the shared template details.

        Example:
            >>> response = await client.email.templates.get_shared(template_id="XXX")
        """
        return await self._client._request("GET", self.previous_root + "/shared-templates/" + template_id, headers=self.headers)

    @validate_call
    async def list_shared(self,
                          page: int = Field(default=1),
                          page_size: int = Field(default=25, ge=1, le=100),
                          tags: Optional[list[str]] = Field(default=None, max_length=5)):
        """
        List shared email templates.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 25.
            tags (list[str], optional): A list of tags to filter by. Defaults to None.

        Returns:
            dict: The API response containing the list of shared templates.

        Example:
            >>> response = await client.email.templates.list_shared(page=1, page_size=10, tags=["tag1", "tag2"])
        """
        params = {
            "page": page,
            "pagesize": page_size,
            "tags": tags
        }

        return await self._client._request("GET", self.previous_root + "/shared-templates", params=params, headers=self.headers)
            
    async def delete(self, template_id: str):
        """
        Delete an email template.

        Args:
            template_id (str): The ID of the template to delete.

        Returns:
            dict: The API response indicating the success of the deletion.

        Example:
            >>> response = await client.email.templates.delete(template_id="XXX")
        """
        return await self._client._request("DELETE", self.root_path + "/" + template_id, headers=self.headers)
            
    async def update(self, template_id: str, data: CreateEmailTemplateRequest):
        """
        Update an existing email template.

        Args:
            template_id (str): The ID of the template to update.
            data (CreateEmailTemplateRequest): The updated template data.

        Returns:
            dict: The API response containing the updated template details.

        Example:
            >>> template_data = CreateEmailTemplateRequest(
            ...     name="Updated Welcome Email",
            ...     source="html",
            ...     body="<html>Updated welcome template content</html>"
            ... )
            >>> response = await client.email.templates.update(template_id="XXX", data=template_data)
        """
        return await self._client._request("PUT", self.root_path + "/" + template_id, data=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)
            
    async def get(self, template_id: str):
        """
        Get a specific email template.

        Args:
            template_id (str): The ID of the template to retrieve.

        Returns:
            dict: The API response containing the template details.

        Example:
            >>> response = await client.email.templates.get(template_id="XXX")
        """
        return await self._client._request("GET", self.root_path + "/" + template_id, headers=self.headers)

    @validate_call
    async def list(self,
                   page: int = Field(default=1),
                   page_size: int = Field(default=25, ge=1, le=100)
                  ):
        """
        List all email templates.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 25.

        Returns:
            dict: The API response containing the list of templates.

        Example:
            >>> response = await client.email.templates.list(page=1, page_size=10)
        """
        params = {
            "page": page,
            "pagesize": page_size
        }

        return await self._client._request("GET", self.root_path, params=params, headers=self.headers)
            
    async def create(self, data: CreateEmailTemplateRequest):
        """
        Create a new email template.

        Args:
            data (CreateEmailTemplateRequest): The template creation request data

        Returns:
            dict: The API response containing the created template details

        Example:
            >>> template_data = CreateEmailTemplateRequest(
            ...     name="Welcome Email",
            ...     source="html",
            ...     body="<html>Welcome template content</html>"
            ... )
            >>> response = await client.email.templates.create(data=template_data)
        """
        return await self._client._request("POST", self.root_path, data=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)