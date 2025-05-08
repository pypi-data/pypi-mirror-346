from uuid import UUID
from typing import Optional, Literal
from pydantic import BaseModel, Field
from naxai.models.voice.voice_flow import (VoiceMail,
                                           Welcome,
                                           Menu,
                                           End)

class CreateCallRequest(BaseModel):
    """
    Represents a request to create a call.
    """
    batch_id : Optional[str] = Field(alias="batchId", max_length=64)
    to: list[str] = Field(max_length=1000)
    from_: str = Field(alias="from", min_length=8, max_length=15)
    language: Literal["fr-FR", "fr-BE", "nl-NL", "nl-BE", "en-GB", "de-DE"]
    voice: Literal["woman", "man"]
    idempotency_key: Optional[str] = Field(alias="idempotencyKey", min_length=1, max_length=128)
    calendar_id: Optional[UUID] = Field(alias="calendarId", default=None)
    scheduled_at: Optional[int] = Field(alias="scheduledAt", default=None)
    machine_detection: Optional[bool] = Field(alias="machineDetection", default=False)
    voicemail: Optional[VoiceMail] = Field(default=None)
    welcome: Welcome = Field(alias="welcome")
    menu: Optional[Menu] = Field(alias="menu", default=None)
    end: Optional[End] = Field(alias="end", default=None)

    class Config:
        """Pydantic configuration for the CreateCallRequest model."""
        validate_by_name = True
        populate_by_name = True
