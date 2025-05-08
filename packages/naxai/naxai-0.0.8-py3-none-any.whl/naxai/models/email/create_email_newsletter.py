from typing import Optional, Literal
from pydantic import BaseModel, Field

#TODO: url validations ( thumbnail, preview )
#TODO: verify required props ( segment_id, source, sender_id, reply_to, etc ...)
#TODO: email validation ( reply_to )

class CreateEmailNewsletterRequest(BaseModel):
    
    name: str = Field(max_length=255)
    scheduled_at: Optional[int] = Field(default=None, alias="scheduledAt")
    source: Optional[Literal["html", "editor"]] = Field(default=None)
    segment_id: Optional[str] = Field(default=None, alias="segmentId")
    sender_id: Optional[str] = Field(default=None, alias="senderId")
    reply_to: Optional[str] = Field(default=None, alias="replyTo")
    subject: Optional[str] = Field(default=None, max_length=255)
    pre_header: Optional[str] = Field(default=None, alias="preheader", max_length=255)
    body: Optional[str] = Field(default=None)
    body_design: Optional[dict] = Field(default=None, alias="bodyDesign")
    thumbnail: Optional[str] = Field(default=None)
    preview: Optional[str] = Field(default=None)

    class Config:
        populate_by_name = True