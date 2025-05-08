from typing import Optional
from pydantic import BaseModel, Field

class BaseObject(BaseModel):
    email: str
    name: str

class SenderObject(BaseObject):
    pass

class DestinationObject(BaseObject):
    pass

class CCObject(BaseObject):
    pass

class BCCObject(BaseObject):
    pass

class Attachment(BaseModel):
    name: str
    content_type: str = Field(alias="contentType")
    data: str


    

class SendTransactionalEmailModel(BaseModel):
    sender: SenderObject
    to: list[DestinationObject] = Field(max_length=1000)
    cc: Optional[list[CCObject]] = Field(max_length=50, default=None)
    bcc: Optional[list[BCCObject]] = Field(max_length=50, default=None)
    reply_to: Optional[str] = Field(max_length=100, default=None, alias="replyTo")
    subject: str
    text: Optional[str] = None
    html: Optional[str] = None
    attachments: Optional[list[Attachment]] = Field(max_length=10, default=None)
    enable_tracking: Optional[bool] = Field(alias="enableTracking", default=None)

    class Config:
        populate_by_name = True