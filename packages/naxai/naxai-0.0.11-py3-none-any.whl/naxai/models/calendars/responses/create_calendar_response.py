from pydantic import BaseModel, Field
from typing import Optional

HOUR_PATTERN = r'^\d{2}:\d{2}$'

class ScheduleObject(BaseModel):
    """Schedule object for creating a calendar"""
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

class CreateCalendarResponse(BaseModel):
    id: str
    name: str
    timezone: Optional[str] = None
    schedule: list[ScheduleObject]
    exclusions: Optional[list] = None