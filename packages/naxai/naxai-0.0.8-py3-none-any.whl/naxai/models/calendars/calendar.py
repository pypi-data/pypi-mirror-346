from typing import Optional
from pydantic import BaseModel, Field

HOUR_PATTERN = r'^\d{2}:\d{2}$'

class ScheduleObject(BaseModel):
    """A model representing a single day's schedule configuration.

    This class defines the schedule settings for a single day, including regular
    and extended hours of operation.

    Attributes:
        day (int): The day of the week (1-7).
        open (bool): Whether the schedule is open on this day.
        start (Optional[str]): The start time in "HH:MM" format. Required if open is True.
        stop (Optional[str]): The end time in "HH:MM" format. Required if open is True.
        extended (Optional[bool]): Whether extended hours are enabled. Defaults to False.
        extension_start (Optional[str]): The start time for extended hours in "HH:MM" format.
            Maps to "extensionStart" in JSON.
        extension_stop (Optional[str]): The end time for extended hours in "HH:MM" format.
            Maps to "extensionStop" in JSON.

    Example:
        >>> schedule = ScheduleObject(
        ...     day=1,
        ...     open=True,
        ...     start="09:00",
        ...     stop="17:00",
        ...     extended=True,
        ...     extension_start="08:00",
        ...     extension_stop="18:00"
        ... )

    Note:
        - Day must be between 1 and 7
        - Time values must follow the format "HH:MM"
        - Extended hours are optional
        - Field names are automatically converted between snake_case (Python) and
          camelCase (JSON) formats
    """
    day: int = Field(ge=1, le=7)
    open: bool
    start: Optional[str] = Field(pattern=HOUR_PATTERN, default=None)
    stop: Optional[str] = Field(pattern=HOUR_PATTERN, default=None)
    extended: Optional[bool] = Field(default=False)
    extension_start: Optional[str] = Field(alias="extensionStart", pattern=HOUR_PATTERN, default=None)
    extension_stop: Optional[str] = Field(alias="extensionStop", pattern=HOUR_PATTERN, default=None)

    class Config:
        """Pydantic config class to enable populating by field name"""
        validate_by_name = True
        populate_by_name = True

class Calendar(BaseModel):
    """A model representing a calendar with schedule and time settings.

    This class defines the structure of a calendar, including its identification,
    scheduling rules, and time-related configurations.

    Attributes:
        id (Optional[str]): The unique identifier of the calendar. Defaults to None.
        name (str): The name of the calendar.
        timezone (Optional[str]): The timezone setting for the calendar. Defaults to Europe/Brussels.
        schedule (list[ScheduleObject]): A list of exactly 7 ScheduleObject instances,
            representing the schedule for each day of the week.
        exclusions (Optional[list[str]]): A list of dates to be excluded from the
            calendar schedule. Defaults to None.

    Example:
        >>> schedule_objects = [
        ...     ScheduleObject(
        ...         day=1,
        ...         open=True,
        ...         start="09:00",
        ...         stop="17:00"
        ...     ),
        ...     # ... repeat for all 7 days
        ... ]
        >>> calendar = Calendar(
        ...     name="Business Hours",
        ...     timezone="UTC",
        ...     schedule=schedule_objects
        ... )

    Note:
        - The schedule must contain exactly 7 ScheduleObject instances (one per day)
        - Time values in ScheduleObject must follow the format "HH:MM"
        - Days in ScheduleObject are numbered 1-7
        - The model uses Pydantic for validation and serialization

    See Also:
        ScheduleObject: The model class used for daily schedule configuration
    """
    id: Optional[str] = None
    name: str
    timezone: Optional[str] = "Europe/Brussels"
    schedule: list[ScheduleObject] = Field(max_length=7, min_length=7)
    exclusions: Optional[list[str]] = None