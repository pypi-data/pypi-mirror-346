from pydantic import BaseModel, Field

class ExclusionResponse(BaseModel):
    """Response model for calendar exclusion addition/deletion operations.

    This class represents the response received after adding/deleting exclusion dates to a calendar.
    It contains the complete list of exclusions for the calendar after the addition/deletion operation.

    Attributes:
        exclusions (list[str]): A list of all exclusion dates for the calendar.
            Each date is represented as a string. This includes both previously existing
            exclusions and newly added ones.

    Example:
        >>> response = AddExclusionResponse(
        ...     exclusions=["2024-12-25", "2024-12-26", "2025-01-01"]
        ... )
        >>> print(response.exclusions)
        ['2024-12-25', '2024-12-26', '2025-01-01']

    Note:
        - The field 'exclusions' is mapped from the JSON key 'exclusions'
        - Dates should be in string format
        - The list contains all exclusions
        - This model is used as the return type for the add_exclusions and delete_exclusions methods

    See Also:
        Calendar: The main calendar model class
    """
    exclusions: list[str] = Field(alias="exclusions")