from .voice import VoiceResource
from .calendars import CalendarsResource
from .email import EmailResource

RESOURCE_CLASSES = {
    "voice": VoiceResource,
    "calendars": CalendarsResource,
    "email": EmailResource
}