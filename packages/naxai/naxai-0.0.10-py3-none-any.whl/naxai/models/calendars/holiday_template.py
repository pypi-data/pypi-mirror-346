from pydantic import BaseModel, Field

class HolidayTemplate(BaseModel):
    """Model representing a holiday template configuration.

    This class defines the structure of a holiday template, which can be used to
    create and manage sets of holiday dates that can be applied to calendars.

    Attributes:
        id (str): The unique identifier of the holiday template.
            Mapped from JSON key 'id'.
        name (str): The name of the holiday template. Limited to 60 characters.
            Mapped from JSON key 'name'.
        dates (list[str]): List of dates included in this holiday template.
            Mapped from JSON key 'dates'.

    Example:
        >>> template = HolidayTemplate(
        ...     id="ht_123abc",
        ...     name="US Federal Holidays 2024",
        ...     dates=[
        ...         "2024-01-01",  # New Year's Day
        ...         "2024-01-15",  # Martin Luther King Jr. Day
        ...         "2024-02-19"   # Presidents' Day
        ...     ]
        ... )
        >>> print(template.name)
        'US Federal Holidays 2024'
        >>> print(len(template.dates))
        3

    Note:
        - The 'id' field is mapped from the JSON key 'id'
        - The 'name' field is mapped from the JSON key 'name'
        - The 'dates' field is mapped from the JSON key 'date'
        - The name field has a maximum length of 60 characters
        - Dates should be provided in a string format
        - This model uses Pydantic's validation and serialization features
    """
    id: str = Field(alias="id")
    name: str = Field(alias="name", max_length=60)
    dates: list[str] = Field(alias="dates")