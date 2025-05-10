from pydantic import BaseModel, Field

class Call(BaseModel):
    call_id: str = Field(alias="callId")
    to: str

class CreateCallResponse(BaseModel):
    batch_id: str = Field(alias="batchId")
    count: int
    calls: list[Call]