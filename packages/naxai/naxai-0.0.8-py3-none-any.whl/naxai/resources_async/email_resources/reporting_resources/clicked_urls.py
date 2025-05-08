import datetime
from typing import Optional, Literal

class ClickedUrlsResource:
    """ cliqued_urls resource for email.reporting resource """

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path + "/clicks"
        self.headers = {"Content-Type": "application/json"}


    async def list(self,
                  start: Optional[int] = int((datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=7)).timestamp()),
                  stop: Optional[int] = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp()),
                  group: Optional[Literal["day", "month"]] = "day",
                  ):
        """
        Retrieves a list of clicked URLs for a given time period and filters.

        Args:
            start (int, optional): The start timestamp for the time period. Defaults to 7 days ago.
            stop (int, optional): The end timestamp for the time period. Defaults to the current time.
            group (literal["day", "month"], optional):  Defaults to "day".

        Returns:
            dict: The API response containing the list of clicked URLs.

        Example:
            >>> response = await client.email reporting.cliqued_urls.list(start=1625097600, stop=1627689600)
        """
        params = {
            "start": start,
            "stop": stop,
            "group": group
        }

        return await self._client._request("GET", self.root_path, params=params, headers=self.headers)
            
    