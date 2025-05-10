from .voice import VoiceResource
from .calendars import CalendarsResource
from .email import EmailResource
from .people import PeopleResource

RESOURCE_CLASSES = {
    "voice": VoiceResource,
    "calendars": CalendarsResource,
    "email": EmailResource,
    "people": PeopleResource
}