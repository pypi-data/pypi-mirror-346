from typing import Optional
from pydantic import BaseModel, Field

class CheckCalendarResponse(BaseModel):
    """Deletes exclusion dates from a calendar.

    This method removes specified dates from the calendar's exclusion list. These dates
    will no longer be considered as non-working days in the calendar.

    Args:
        calendar_id (str): The unique identifier of the calendar to update.
        exclusions (list[str]): List of dates to remove from the calendar's exclusions.
            Each date should be in a string format. Maximum of 1000 dates
            can be removed in a single request.

    Returns:
        ExclusionResponse: An object containing:
            - exclusions (list[str]): The complete list of remaining exclusions for 
              the calendar after removing the specified dates.

    Raises:
        APIError: If there is an error response from the API.
        ValidationError: If the request data or response cannot be properly validated.
        NotFoundError: If the calendar with the specified ID doesn't exist.
        ConnectionError: If there are network connectivity issues.
        NaxaiValueError: If more than 1000 exclusions are provided.

    Example:
        >>> dates_to_remove = ["2024-12-25", "2024-12-26"]
        >>> result = client.calendars.delete_exclusions(
        ...     "cal_123abc",
        ...     exclusions=dates_to_remove
        ... )
        >>> print(result.exclusions)  # Shows remaining exclusions after deletion

    Note:
        - The request is made with "Content-Type: application/json" header
        - Maximum of 1000 exclusions can be deleted in a single request
        - The endpoint used is "{root_path}/calendars/{calendar_id}/exclusions/remove"
        - Non-existent dates in the exclusion list are ignored
        - The response includes all remaining exclusions after the deletion

    See Also:
        Calendar: The main calendar model class
        ExclusionResponse: The response model containing updated exclusions list
        add_exclusions: Method to add exclusion dates to a calendar
    """
    match_: bool = Field(alias="match")
    next_: Optional[int] = Field(alias="next", default=None)

    class Config:
        populate_by_name = True
        validate_by_name = True