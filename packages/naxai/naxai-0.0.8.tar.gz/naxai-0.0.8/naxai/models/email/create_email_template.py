from typing import Optional, Literal
from pydantic import BaseModel, Field

#TODO: url validation (thumbnail)
#TODO: verify required properties
class CreateEmailTemplateRequest(BaseModel):
    name: str = Field(max_length=255)
    source: Optional[Literal["html", "editor"]] = Field(default=None)
    body: Optional[str] = Field(default=None)
    body_design: Optional[dict] = Field(default=None, alias="bodyDesign")
    thumbnail: Optional[str] = Field(default=None)

    