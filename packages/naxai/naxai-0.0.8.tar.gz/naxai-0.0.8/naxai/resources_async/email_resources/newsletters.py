from naxai.models.email.create_email_newsletter import CreateEmailNewsletterRequest
from pydantic import Field, validate_call

class NewslettersResource:
    """ newsletters resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/newsletters"
        self.headers = {"Content-Type": "application/json"}
            
    async def create(self, data:CreateEmailNewsletterRequest):
        """
        Create a new email newsletter.

        Args:
            data: (CreateEmailNewsletterRequest) : Containing the request body to create a newsletter

        Returns:
            dict: The API response containing the created newsletter details

        Example:
            >>> response = await client.email.newsletters.create(
            ...     data=CreateEmailNewsletterRequest(
            ...         name="XXXX",
            ...         ...)
            ... )
        """
        return await self._client._request("POST", self.root_path, data=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)
    
    @validate_call
    async def list(self, page: int = 1, page_size: int = Field(default=25, le=100, ge=1)):
        """
        List all email newsletters.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 50.

        Returns:
            dict: The API response containing the list of newsletters.

        Example:
            >>> response = await client.email.newsletters.list(page=1, page_size=50)
        """
        params = {
            "page": page,
            "pagesize": page_size
        }
        return await self._client._request("GET", self.root_path, params=params, headers=self.headers)
    
    async def get(self, newsletter_id: str):
        """
        Get details of a specific email newsletter.

        Args:
            newsletter_id (str): The ID of the newsletter to retrieve.

        Returns:
            dict: The API response containing the newsletter details.

        Example:
            >>> response = await client.email.newsletters.get(newsletter_id="XXXX")
        """
        return await self._client._request("GET", self.root_path + "/" + newsletter_id, headers=self.headers)
    
    async def update(self, data: CreateEmailNewsletterRequest, newsletter_id: str):
        """
        Update an existing email newsletter.

        Args:
            data (CreateEmailNewsletterRequest): The updated data for the newsletter.
            newsletter_id (str): The ID of the newsletter to update.

        Returns:
            dict: The API response containing the updated newsletter details.

        Example:
            >>> response = await client.email.newsletters.update(
            ...     data=CreateEmailNewsletterRequest(
            ...         name="XXXX",
            ...         ...)
            ...     newsletter_id="XXXX"
            ... )
        """
        return await self._client._request("PUT", self.root_path + "/" + newsletter_id, data=data.model_dump(by_alias=True, exclude_none=True), headers=self.headers)
    
    async def delete(self, newsletter_id: str):
        """
        Delete an existing email newsletter.

        Args:
            newsletter_id (str): The ID of the newsletter to delete.

        Returns:
            dict: The API response indicating the deletion status.

        Example:
            >>> response = await client.email.newsletters.delete(newsletter_id="XXXX")
        """
        return await self._client._request("DELETE", self.root_path + "/" + newsletter_id, headers=self.headers)