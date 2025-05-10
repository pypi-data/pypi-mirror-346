from typing import Optional, Literal
from pydantic import BaseModel, Field



class End(BaseModel):
    """ End Model """
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given

class Whisper(BaseModel):
    """ Whisper Model """
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given

class Transfer(BaseModel):
    """ Transfer Model """
    destination: str = Field(alias="destination")
    attempts: Optional[int] = Field(alias="attempts", default=1, ge=1, le=3)
    timeout: Optional[int] = Field(alias="timeout", default=15, ge=5, le=30)
    whisper: Optional[Whisper] = Field(alias="whisper", default=None)

class Choice(BaseModel):
    """ Choice Model """
    key: Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#"]
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given
    replay: Optional[int] = Field(alias="replay", default=0)
    transfer: Optional[Transfer] = Field(alias="transfer", default=None)

class Menu(BaseModel):
    """ Menu Model """
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given
    replay: Optional[int] = Field(alias="replay", default=0)
    choices: list[Choice] = Field(alias="choices")

class Welcome(BaseModel):
    """ Welcome Model """
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given
    replay: Optional[int] = Field(alias="replay", default=0)

class VoiceMail(BaseModel):
    """ Voicemail Model"""
    say: Optional[str] = Field(alias="say", default=None)
    prompt: Optional[str] = Field(alias="prompt", default=None) # check if it's an url that is given

class VoiceFlow(BaseModel):
    """VoiceFlow model"""
    machine_detection: Optional[bool] = Field(alias="machineDetection", default=False)
    voicemail: Optional[VoiceMail] = Field(default=None)
    welcome: Welcome = Field(alias="welcome")
    menu: Optional[Menu] = Field(alias="menu", default=None)
    end: Optional[End] = Field(alias="end", default=None)