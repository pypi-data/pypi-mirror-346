import datetime
from typing import Literal, Optional
from pydantic import Field, validate_call

class EventsResource:
    """ events resource for people.contacts resource"""

    def __init__(self, client, root_path):
        self._client = client
        self.root_path = root_path
        self.headers = {"Content-Type": "application/json"}

    @validate_call
    async def send(self,
                identifier: str,
                name: Optional[str] = None,
                type_: Optional[Literal["event"]] = Field(default=None, alias="type"),
                timestamp: Optional[int] = datetime.datetime.now(tz=datetime.timezone.utc),
                idempotency_key: Optional[str] = Field(default=None, max_length=200),
                data: Optional[dict[str,str]] = None):
         
        """
        Send events for a contact.

        Args:
            identifier (str): The unique identifier of the contact.
            name (str, optional): The name of the event.
            type (Literal["event"], optional): The type of the event.
            timestamp (int, optional): The timestamp of the event. Defaults to the current UTC time.
            idempotency_key (str, optional): The idempotency key for the event.
            data (dict[str,str], optional): Additional data for the event.

        Returns:
            dict: The API response containing the event details.

        Raises:
            ValueError: If the identifier is empty.
            APIError: If there is an error response from the API.

        Example:
            >>> response = client.people.contacts.send_events(
            ...     identifier="XXXX",
            ...     name="XXXX",
            ...     type="XXXX",
            ...     timestamp=XXXX,
            ...     idempotency_key="XXXX",
            ...     data={"XXXX": "XXXX"}
            ... )
        """
        data = {
            "name": name,
            "type": type_,
            "timestamp": timestamp,
            "idempotencyKey": idempotency_key,
            "data": data
        }

        return await self._client._request("POST", self.root_path + "/" + identifier + "/events", json=data, headers=self.headers)
