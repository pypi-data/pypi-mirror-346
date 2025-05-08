from typing import Optional, Literal
from pydantic import Field, validate_call

class ActivityLogsResource:
    """ activity_logs resource for email resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/activity-logs"
        self.headers = {"Content-Type": "application/json"}
            
    #TODO: email validation
    async def get(self, message_id: str, email: str):
        """
        Retrieves an activity log by message ID and email address.

        Args:
            message_id (str): The ID of the message.
            email (str): The email address.

        Returns:
            dict: The API response containing the activity log.

        Example:
            >>> response = await client.email.activity_logs.get(message_id="XXX", email="example@example.com")
        """


        return await self._client._request("GET", self.root_path + "/" + message_id + "/" + email, headers=self.headers)
    
    #TODO: email validation
    @validate_call
    async def list(self,
                   page: Optional[int] = 1,
                   page_size: Optional[int] = Field(default=50, ge=1, le=100),
                   start: Optional[int] = None,
                   stop: Optional[int] = None,
                   sort: Optional[str] = "updatedAt:desc",
                   email: Optional[str] = None,
                   client_id: Optional[str] = None,
                   campaign_id: Optional[str] = None,
                   status: Optional[Literal["sent", "delivered", "failed"]] = None
                   ):
        """
        Retrieves a list of activity logs for a given time period and filters.

        Args:
            page (int, optional): The page number to retrieve. Defaults to 1.
            page_size (int, optional): The number of items per page. Defaults to 100.
            start (int, optional): The start timestamp for the time period.
            stop (int, optional): The end timestamp for the time period.
            sort (str, optional): The sort order for the activity logs. Defaults to "updatedAt:desc".
            email (str, optional): The email address to filter on.
            client_id (str, optional): The client ID to filter on.
            campaign_id (str, optional): The campaign ID to filter on.
            status (literal["sent", "delivered", "failed"], optional): The status to filter on.

        Returns:
            dict: The API response containing the list of activity logs.

        Example:
            >>> response = await client.email.activity_logs.list(start=1625097600, stop=1627689600)
        """
        params = {
            "page": page,
            "pagesize": page_size,
            "sort": sort
        }

        if start:
             params["start"] = start
        if stop:
             params["stop"] = stop
        if email:
             params["email"] = email
        if client_id:
             params["clientId"] = client_id
        if campaign_id:
             params["campaignId"] = campaign_id
        if status:
             params["status"] = status

        return await self._client._request("GET", self.root_path, params=params, headers=self.headers)